# Business_Intelligence_Bot

## Overview
This project is an all-in-one Business Intelligence Bot, which can automate a lot of repitiitve tasks required for the operations of a business. The bot receives and answers queries through Telegram. The bot can extract stock of a product from the database, generate well-formatted quotations in PDF format and many others. It is built using LangChain, LangGraph, PostgreSQL, as well as n8n, to connect it to Telegram. 

## System Architecture

<img width="652" height="333" alt="image" src="https://github.com/user-attachments/assets/547b49ce-d71b-484c-a49b-a6dca38fa4a9" />

## Technology Stack

* LangChain
* LangGraph
* PostgreSQL
* Gemini models
* n8n
* Telegram

## Agents

### Fetch Stock Agent

This agent fetches data from Google Sheet, and returns the stock quantity of the requested product. The agent calls the following tool:
1. get_sheets_data: This tool can access the Google Sheet containing the stock data, and read data from it

### Quotation Agent

This agent can generate quotations for multiple services (like flooring, paint etc). The user can provide the dimensoins of the area in either the text itself, or an image of a technical drawing. The agent returns the HTML code for generating the quotation. The agent has access to the following tools:
1. get_price_data: This tool can access the Google Sheet containing the per sq meter




