# University Application Chatbot

## Overview

The University Application Chatbot streamlines the application process using a sophisticated architecture. Files are parsed, organized into sections, and stored on Azure Blob Service. The Hoya Search AI service indexes sections for efficient retrieval. LangChain connects to Azure OpenAI, utilizing Azure Search AI and Form Recognizer to locate relevant PDF sections. The obtained information is used to train the Azure LLM for accurate, conversational responses.

## Architecture

### 1. File Parsing and Storage

- **Parser:**
  - Breaks files into pages, extracting relevant information.
  - Organizes content into sections for effective storage.

- **Azure Blob Service:**
  - Stores parsed files and sections for seamless accessibility.

### 2. Hoya Search AI

- **Indexing:**
  - Hoya Search AI efficiently indexes sections for quick retrieval.

### 3. LangChain Model

- **OpenAI Integration:**
  - Connects to Azure OpenAI resource for natural language processing.

- **Azure Search AI Integration:**
  - Utilizes Azure Search AI to find relevant PDF sections based on user prompts.

- **Form Recognizer:**
  - Extracts information from PDF sections using Form Recognizer.

- **Context Passing:**
  - LangChain passes context to Azure LLM, ensuring accurate responses.

### 4. Azure Large Language Model (LLM)

- **Training:**
  - Receives context from LangChain for personalized and context-aware responses.

## Features

### 1. Efficient Search

- Users can prompt the chatbot for specific information within PDF sections.
- Hoya Search AI ensures quick and accurate retrieval of relevant content.

### 2. Context-Aware Responses

- LangChain facilitates the passing of context to Azure LLM.
- Conversational responses are trained on the latest information for a personalized user experience.


## Usage

- Users interact with the chatbot, asking questions or seeking information.
- The chatbot utilizes the intricate architecture to provide accurate, context-aware responses.

## Future Enhancements

- **Enhanced Search Capabilities:** Implement advanced search features for more nuanced queries.
- **Real-time Training:** Explore options for continuous training to keep responses up-to-date.

## Conclusion

The University Application Chatbot, powered by an intricate architecture, revolutionizes information retrieval for streamlined application processes. From file parsing to AI-driven responses, each component contributes to a seamless and intelligent user experience.
