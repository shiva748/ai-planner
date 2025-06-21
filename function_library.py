import os
from typing import List, Dict
from pydantic import BaseModel

class FunctionDescription(BaseModel):
    name: str
    description: str
    inputs: Dict[str, str]
    outputs: Dict[str, str]

function_library = [
    {"name": "retrieve_invoices", "description": "Retrieve all invoices for a given month.", "inputs": {"month": "str"}, "outputs": {"invoices": "List[Invoice]"}},
    {"name": "summarize_invoices", "description": "Summarize total amount from a list of invoices.", "inputs": {"invoices": "List[Invoice]"}, "outputs": {"summary": "str"}},
    {"name": "send_email", "description": "Send an email with the provided content.", "inputs": {"recipient": "str", "content": "str"}, "outputs": {"status": "str"}},
    {"name": "get_user_profile", "description": "Retrieve user profile information.", "inputs": {"user_id": "str"}, "outputs": {"profile": "UserProfile"}},
    {"name": "update_user_profile", "description": "Update user profile fields.", "inputs": {"user_id": "str", "fields": "dict"}, "outputs": {"status": "str"}},
    {"name": "list_projects", "description": "List all projects for a user.", "inputs": {"user_id": "str"}, "outputs": {"projects": "List[Project]"}},
    {"name": "create_project", "description": "Create a new project.", "inputs": {"user_id": "str", "project_name": "str"}, "outputs": {"project_id": "str"}},
    {"name": "delete_project", "description": "Delete a project by ID.", "inputs": {"project_id": "str"}, "outputs": {"status": "str"}},
    {"name": "add_task", "description": "Add a new task to a project.", "inputs": {"project_id": "str", "task_name": "str"}, "outputs": {"task_id": "str"}},
    {"name": "update_task_status", "description": "Update the status of a task.", "inputs": {"task_id": "str", "status": "str"}, "outputs": {"status": "str"}},
    {"name": "list_tasks", "description": "List all tasks in a project.", "inputs": {"project_id": "str"}, "outputs": {"tasks": "List[Task]"}},
    {"name": "assign_task", "description": "Assign a task to a user.", "inputs": {"task_id": "str", "user_id": "str"}, "outputs": {"status": "str"}},
    {"name": "set_task_deadline", "description": "Set a deadline for a task.", "inputs": {"task_id": "str", "deadline": "str"}, "outputs": {"status": "str"}},
    {"name": "get_task_details", "description": "Get details of a specific task.", "inputs": {"task_id": "str"}, "outputs": {"task": "Task"}},
    {"name": "delete_task", "description": "Delete a task by ID.", "inputs": {"task_id": "str"}, "outputs": {"status": "str"}},
    {"name": "search_documents", "description": "Search documents by keyword.", "inputs": {"keyword": "str"}, "outputs": {"documents": "List[Document]"}},
    {"name": "upload_document", "description": "Upload a new document.", "inputs": {"user_id": "str", "file": "File"}, "outputs": {"document_id": "str"}},
    {"name": "download_document", "description": "Download a document by ID.", "inputs": {"document_id": "str"}, "outputs": {"file": "File"}},
    {"name": "delete_document", "description": "Delete a document by ID.", "inputs": {"document_id": "str"}, "outputs": {"status": "str"}},
    {"name": "generate_report", "description": "Generate a report from data.", "inputs": {"data": "Any", "report_type": "str"}, "outputs": {"report": "Report"}},
    {"name": "send_sms", "description": "Send an SMS message.", "inputs": {"phone_number": "str", "content": "str"}, "outputs": {"status": "str"}},
    {"name": "schedule_meeting", "description": "Schedule a meeting with participants.", "inputs": {"participants": "List[str]", "datetime": "str"}, "outputs": {"meeting_id": "str"}},
    {"name": "cancel_meeting", "description": "Cancel a scheduled meeting.", "inputs": {"meeting_id": "str"}, "outputs": {"status": "str"}},
    {"name": "list_meetings", "description": "List all meetings for a user.", "inputs": {"user_id": "str"}, "outputs": {"meetings": "List[Meeting]"}},
    {"name": "get_weather", "description": "Get the weather for a location.", "inputs": {"location": "str"}, "outputs": {"weather": "WeatherInfo"}},
    {"name": "get_news", "description": "Get the latest news headlines.", "inputs": {"topic": "str"}, "outputs": {"headlines": "List[str]"}},
    {"name": "translate_text", "description": "Translate text to a target language.", "inputs": {"text": "str", "target_language": "str"}, "outputs": {"translation": "str"}},
    {"name": "convert_currency", "description": "Convert an amount from one currency to another.", "inputs": {"amount": "float", "from_currency": "str", "to_currency": "str"}, "outputs": {"converted_amount": "float"}},
    {"name": "calculate_sum", "description": "Calculate the sum of a list of numbers.", "inputs": {"numbers": "List[float]"}, "outputs": {"sum": "float"}},
    {"name": "calculate_average", "description": "Calculate the average of a list of numbers.", "inputs": {"numbers": "List[float]"}, "outputs": {"average": "float"}},
    {"name": "find_maximum", "description": "Find the maximum value in a list of numbers.", "inputs": {"numbers": "List[float]"}, "outputs": {"max": "float"}},
    {"name": "find_minimum", "description": "Find the minimum value in a list of numbers.", "inputs": {"numbers": "List[float]"}, "outputs": {"min": "float"}},
    {"name": "sort_numbers", "description": "Sort a list of numbers.", "inputs": {"numbers": "List[float]", "order": "str"}, "outputs": {"sorted_numbers": "List[float]"}},
    {"name": "filter_even_numbers", "description": "Filter even numbers from a list.", "inputs": {"numbers": "List[int]"}, "outputs": {"even_numbers": "List[int]"}},
    {"name": "filter_odd_numbers", "description": "Filter odd numbers from a list.", "inputs": {"numbers": "List[int]"}, "outputs": {"odd_numbers": "List[int]"}},
    {"name": "count_items", "description": "Count the number of items in a list.", "inputs": {"items": "List[Any]"}, "outputs": {"count": "int"}},
    {"name": "find_duplicates", "description": "Find duplicate items in a list.", "inputs": {"items": "List[Any]"}, "outputs": {"duplicates": "List[Any]"}},
    {"name": "remove_duplicates", "description": "Remove duplicate items from a list.", "inputs": {"items": "List[Any]"}, "outputs": {"unique_items": "List[Any]"}},
    {"name": "merge_lists", "description": "Merge two lists into one.", "inputs": {"list1": "List[Any]", "list2": "List[Any]"}, "outputs": {"merged_list": "List[Any]"}},
    {"name": "split_text", "description": "Split text by a delimiter.", "inputs": {"text": "str", "delimiter": "str"}, "outputs": {"parts": "List[str]"}},
    {"name": "join_text", "description": "Join a list of strings into text with a delimiter.", "inputs": {"parts": "List[str]", "delimiter": "str"}, "outputs": {"text": "str"}},
    {"name": "capitalize_text", "description": "Capitalize the first letter of each word in text.", "inputs": {"text": "str"}, "outputs": {"capitalized": "str"}},
    {"name": "reverse_text", "description": "Reverse the characters in a string.", "inputs": {"text": "str"}, "outputs": {"reversed": "str"}},
    {"name": "generate_uuid", "description": "Generate a new UUID.", "inputs": {}, "outputs": {"uuid": "str"}},
    {"name": "get_current_datetime", "description": "Get the current date and time.", "inputs": {}, "outputs": {"datetime": "str"}},
    {"name": "format_datetime", "description": "Format a datetime string.", "inputs": {"datetime": "str", "format": "str"}, "outputs": {"formatted": "str"}},
    {"name": "parse_json", "description": "Parse a JSON string into an object.", "inputs": {"json_str": "str"}, "outputs": {"obj": "Any"}},
    {"name": "stringify_json", "description": "Convert an object to a JSON string.", "inputs": {"obj": "Any"}, "outputs": {"json_str": "str"}},
    {"name": "compress_text", "description": "Compress a string using gzip.", "inputs": {"text": "str"}, "outputs": {"compressed": "bytes"}},
    {"name": "decompress_text", "description": "Decompress a gzip-compressed string.", "inputs": {"compressed": "bytes"}, "outputs": {"text": "str"}},
    {"name": "encrypt_text", "description": "Encrypt text with a password.", "inputs": {"text": "str", "password": "str"}, "outputs": {"encrypted": "str"}},
    {"name": "decrypt_text", "description": "Decrypt text with a password.", "inputs": {"encrypted": "str", "password": "str"}, "outputs": {"text": "str"}},
]

def get_function_library():
    return function_library
