# AI Business Assistant

## Overview
An AI-powered business assistant that automates common operational tasks through Telegram, including inventory lookup, quotation generation, document retrieval, and product image retrieval using a multi-agent LangGraph architecture. It is built using LangChain, LangGraph, PostgreSQL, as well as n8n, to connect it to Telegram. 

## System Architecture

<img width="652" height="333" alt="image" src="https://github.com/user-attachments/assets/547b49ce-d71b-484c-a49b-a6dca38fa4a9" />

## Technology Stack

* LangChain
* LangGraph
* PostgreSQL
* Gemini models
* FastAPI
* n8n
* Telegram

## Agents

### Supervisor Agent
This agent understands the user query and calls the appropriate worker agent.

### Fetch Stock Agent

This agent fetches data from Google Sheet, and returns the stock quantity of the requested product. The agent has access to the following tool:
1. get_sheets_data: This tool can access the Google Sheet containing the stock data, and read data from it

### Quotation Agent

This agent can generate quotations for multiple services (like flooring, paint etc). The user can provide the dimensions of the area in either the text itself, or an image of a technical drawing. The agent returns the HTML code for generating the quotation. The agent has access to the following tools:
1. get_price_data: This tool can reads pricing information from Google Sheets containing the per sq meter rate of various services, and returns the rate of that service.
2. convert_cm_to_m: This tool converts the given length from cm to m
3. calculate_total_cost: This tool calculates the total price based on the length, width and rate per sq m.
4. calculate_grand_total: This tool calculates the grand total of all the services.
5. generate_quotation_tool: This tool inserts all the services data in a HTML quotation template, and returns the final HTML code

### Image Agent

This agent extracts the image of the requested service from PostgreSQL database, and returns its public URL. The images of all the services are stored in Supabase Storage. The agent has access to the following tool:
1. get_image: Extracts the file path of the image of that product from a supabase table, then returns the public URL of the image

### RAG Agent

This agent retrieves the similar chunks from Supabase table, and generates a formal answer using that context. The agent has access to the following tool:
1. retrieve_docs: Retrieves and returns 2 most similar chunks from the whole document

## LangGraph

A graph using LangGraph is designed to orchestrate the agents. The graph is exposed using a FastAPI server, which can then be accessed by n8n.

## Telegram and n8n
Telegram is used as an interaction medium between the user and the bot. The LangGraph graph, which is the heart of the bot, is connected to Telegram using n8n. 
Here is the workflow in n8n:
1. The workflow is triggered once a user sends a message to the Telegram bot.
2. If the query contains an image, the image is downloaded, and then sent in the binary format to the graph.
3. The graph is invoked using the input message and the input image (if present), using FastAPI
4. The output of the graph is displayed to the user. If the output contains an image, the image is downloaded and sent through Telegram. If the output contains the HTML code, then the HTML code is converted to PDF using HTML2PDF API, and the PDF is then sent through Telegram.






