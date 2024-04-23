# RAG Agent Streamlit Application

## Overview
This repository hosts the Streamlit application for a Retrieval-Augmented Generation (RAG) Agent. The application is specifically tailored to assist architects and construction professionals in navigating the complex New York City Building Code. By combining the benefits of retrieval-based and generative AI models, the RAG model provides enhanced information retrieval and generation capabilities, making it easier to find accurate answers and solutions directly related to the NYC Building Code.

![UI](img/ui.png)

## Features
- **Interactive UI**: Utilize Streamlit to interact with the RAG model in real-time, enhancing the user experience and making it easier to navigate complex regulations.
- **Custom Queries**: Architects can submit queries regarding specific sections of the NYC Building Code and receive responses that blend retrieved data with intelligently generated text, ensuring both accuracy and context.
- **Agent**: View how the RAG model processes and retrieves information, providing insights into the connection between your queries and the code references.
- **NYC Building Code Integration**: Specifically designed to query and interpret the NYC Building Code, helping professionals understand and apply regulations efficiently.

## Installation
To get the application running locally, follow these steps:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/szafranskifilip/RAG_agent_streamlit.git
   cd RAG_agent_streamlit
   ```

2. **Install Requirements**
    ```bash
    pip install -r requirements.txt
    ```
3. Run the Streamlit Application
    ```bash
    streamlit run app.py
    ```

## Usage
Once the application is running, navigate to http://localhost:8501 in your web browser to start interacting with the RAG agent. Input your questions about the NYC Building Code in the provided text box and submit them to see how the agent responds with detailed, context-rich information.

Remember to update the environment variable with your OPENAI_KEY

## License
This project is licensed under the MIT License - see the LICENSE file for details.