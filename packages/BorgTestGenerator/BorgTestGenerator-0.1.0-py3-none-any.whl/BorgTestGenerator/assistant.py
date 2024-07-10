#!/usr/bin/env python3
#coding: utf-8

from openai import OpenAI
from os import getenv

class Assistant(object):
    
    def __init__(self, assistant_id):
        self.client = OpenAI(api_key=getenv("OPENAI_API_KEY"))
        self.assistant_id = assistant_id

    def load_assistant(self):
        self.assistant = self.client.beta.assistants.retrieve(f"{self.assistant_id}")
        return self

    def create_thread(self):
        self.thread = self.client.beta.threads.create()
        return self

    def create_message(self, role, content):
        self.message = self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role=f"{role}",
            content=f"{content}"
        )
        return self

    def create_run(self):
        self.run = self.client.beta.threads.runs.create_and_poll(
            assistant_id=self.assistant.id,
            thread_id=self.thread.id
        )
        #print(self.run)
        return self


    def upload_files(self, files_to_upload, vector_store_name):
        if type(files_to_upload) == str:
            files_to_upload = [files_to_upload]


        # Create a vector store caled "Financial Statements"
        self.vector_store = self.client.beta.vector_stores.create(name=vector_store_name)
 
        # Ready the files for upload to OpenAI
        self.file_paths = files_to_upload
        self.file_streams = [open(path, "rb") for path in self.file_paths]
 
        # Use the upload and poll SDK helper to upload the files, add them to the vector store,
        # and poll the status of the file batch for completion.
        self.file_batch = self.client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=self.vector_store.id, files=self.file_streams
        )
 
        # You can print the status and the file counts of the batch to see the result of this operation.
        #print(self.file_batch.status)
        #print(self.file_batch.file_counts)
        return self

    def update_assistant_with_vector_store(self):
        self.assistant = self.client.beta.assistants.update(
            assistant_id = self.assistant.id,
            tool_resources = {"file_search": {"vector_store_ids": [self.vector_store.id]}},
        )
        return self

    def get_assistant_messages(self):
        if self.run.status == 'completed': 
            self.messages = self.client.beta.threads.messages.list(
                thread_id=self.thread.id
            )
            return self.messages.data[0].content[0].text.value
        else:
            return self.run.status