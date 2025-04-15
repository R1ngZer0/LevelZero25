"""
Implements the Document Writer Agent logic, orchestrating the use of 
document creation tools (Outline, Section Writer, Report Writer) and QA.
"""

from typing import List
from pydantic import BaseModel

from app.schemas.qa_schemas import QAInput
from app.agents.qa_agent import review_content
from app.agents.doc_writer_tools import (
    create_document_outline, 
    write_document_section, 
    format_and_save_report,
    SectionContent, # Import SectionContent model
    ReportOutput    # Import ReportOutput model
)
# Placeholder imports for RAG and vectorization - replace with actual implementations
from app.agents.chatbot_agent import retrieve_rag_context # Use chatbot's RAG for now
# Need functions to handle vectorization based on file path/content
# from app.services.vector_store import add_vector_embedding # Requires DB session and chunking
from app.services.file_processing import extract_text_from_file, chunk_text # Need these
from app.services.vector_store_service import add_embeddings_for_chunks # Assume a higher-level service
from app.services import file_service # To get file metadata
from app.db.session import get_db # For DB session
from app.llm_clients import get_embedding_client # To get model name


MAX_REVISIONS = 3 # Same as chatbot

class DocumentCreationResult(BaseModel):
    """Result object for the document creation process."""
    message: str
    file_path: str | None = None # Path to the final .docx file

def create_document(prompt: str, mode: str = "cloud") -> DocumentCreationResult:
    """Orchestrates the document creation process."""
    print(f"--- Starting Document Creation for Prompt: '{prompt[:50]}...' ---")
    approved_sections: List[SectionContent] = []
    document_title = "Untitled Document"
    final_report: ReportOutput | None = None
    db_session_context = None # For managing DB session scope

    try:
        # 1. Retrieve RAG context (optional, based on prompt)
        # For simplicity, we use the chatbot's RAG logic here.
        rag_context = retrieve_rag_context(prompt, []) # Pass empty history for now
        print(f"Retrieved RAG context: {rag_context[:100]}...")

        # 2. Create Outline
        print("Generating outline...")
        outline = create_document_outline(prompt=prompt, context=rag_context, mode=mode)
        document_title = outline.title
        print(f"Outline generated: Title - '{document_title}', Topics - {[t.heading for t in outline.topics]}")

        # 3. Loop through topics, write sections with QA
        for i, topic in enumerate(outline.topics):
            print(f"--- Writing Section {i+1}/{len(outline.topics)}: '{topic.heading}' ---")
            current_section_content: SectionContent | None = None
            feedback: str | None = None
            
            for attempt in range(MAX_REVISIONS + 1):
                print(f"Section '{topic.heading}' - Attempt {attempt + 1}")
                
                # Prepare input for section writer
                section_prompt = prompt 
                if feedback:
                     # Pass feedback directly in the section writer args? No, modify prompt.
                     current_prompt = f"{prompt}\n\n## Previous Attempt Feedback (Please Address):\n{feedback}"
                else:
                     current_prompt = prompt

                # Call Section Writer Tool
                # Make sure to pass only approved sections for context
                current_section_content = write_document_section(
                    topic_heading=topic.heading,
                    full_prompt=current_prompt, # Pass potentially modified prompt
                    document_title=document_title,
                    previous_sections=approved_sections, # Pass previously approved sections
                    context=rag_context, 
                    mode=mode
                )
                
                # Submit section to QA
                qa_input = QAInput(
                    content_to_review=current_section_content.content,
                    original_prompt=f"Write content for section: {topic.heading} (part of document: {document_title})",
                    context=rag_context # Pass relevant context
                )
                qa_result = review_content(qa_input, mode=mode)
                
                if qa_result.is_approved:
                    print(f"QA approved section '{topic.heading}' on attempt {attempt + 1}")
                    approved_sections.append(current_section_content) # Add to approved list
                    feedback = None
                    break # Move to next section
                else:
                    feedback = qa_result.feedback
                    print(f"QA requires revision for section '{topic.heading}': {feedback}")
                    if attempt == MAX_REVISIONS:
                        print(f"Max revisions reached for section '{topic.heading}'. Discarding section and stopping document generation.")
                        raise RuntimeError(f"Failed to get QA approval for section '{topic.heading}' after {MAX_REVISIONS + 1} attempts.")
            
            # This check ensures the loop didn't somehow exit without approving a section (e.g., if break was missed)
            if feedback is not None: # If feedback is still set, it means the loop finished without approval
                 raise RuntimeError(f"Loop finished for section '{topic.heading}' without QA approval.")
                 
        # 4. Format and Save Final Report
        print("--- Formatting and Saving Final Report ---")
        if not approved_sections:
            raise ValueError("No sections were approved. Cannot generate final report.")
            
        final_report = format_and_save_report(
            document_title=document_title,
            sections=approved_sections
        )
        print(f"Final report saved to: {final_report.file_path}")

        # 5. Vectorize Final Document
        print(f"--- Vectorizing Final Document: {final_report.file_path} ---")
        try:
            db_session_context = get_db()
            db = next(db_session_context)

            # Assume file_service can get or create file metadata based on path
            # This might need adjustment based on file_service implementation
            file_meta = file_service.get_file_by_path(db, final_report.file_path)
            if not file_meta:
                 # If the file wasn't tracked before (likely), create metadata entry
                 # Need a function like `upsert_file_metadata` or similar in file_service
                 print(f"Warning: File metadata not found for {final_report.file_path}. Vectorization might fail without file_id.")
                 # Simplified: skip vectorization if metadata missing. Needs proper handling.
                 raise ValueError(f"File metadata not found for generated document: {final_report.file_path}")

            # Use the full text returned by the report writer tool
            full_doc_text = final_report.full_text 
            
            # Chunk the text (using existing service)
            text_chunks = chunk_text(full_doc_text)
            print(f"Document chunked into {len(text_chunks)} chunks for vectorization.")

            # Get embedding model based on mode (or config)
            embedding_client = get_embedding_client() # Uses configured client
            embedding_model_name = embedding_client.model

            # Add embeddings (using a hypothetical higher-level service)
            # This service would handle batching and DB interactions
            add_embeddings_for_chunks(
                db=db,
                file_id=file_meta.id,
                text_chunks=text_chunks,
                embedding_model_name=embedding_model_name
            )
            print(f"Successfully added embeddings for {final_report.file_path}")

        except Exception as e:
            print(f"Error during vectorization of the final document: {e}")
            # Log error but don't fail the whole process? Or raise?
            # For now, just log it.
        finally:
            if db_session_context:
                try:
                    next(db_session_context, None) # Consume the rest of the generator
                except StopIteration:
                    pass
                except Exception as e:
                     print(f"Error closing DB session context after vectorization: {e}")

        # --- Document Creation Successful ---
        return DocumentCreationResult(
            message=f"Document '{document_title}' created successfully.",
            file_path=final_report.file_path
        )

    except Exception as e:
        print(f"--- Document Creation Failed: {e} ---")
        # Log the full error/stack trace here
        return DocumentCreationResult(
            message=f"Document creation failed: {e}",
            file_path=None
        )

# Placeholder for vectorization service function
# Replace with actual import from vector_store_service.py when implemented
def add_embeddings_for_chunks(db, file_id, text_chunks, embedding_model_name):
     print(f"Placeholder: Would add {len(text_chunks)} embeddings for file {file_id} using {embedding_model_name}")
     pass 