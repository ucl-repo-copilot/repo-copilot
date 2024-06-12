from autogen import AssistantAgent, UserProxyAgent

llm_config = {
  "model": "llama3", 
  "base_url": "http://localhost:11434/v1",
  "api_key": "ollama",
}

assistant = AssistantAgent(
  name="assistant",
  system_message="You are an AI developed to assist with generating tests for Python programs",
  #system_message="You are a documentation generator for Python programs",
  llm_config=llm_config
) # the assistant agent

user_proxy = UserProxyAgent(
  name="user_proxy", 
  code_execution_config=False
)

documentationPromptTemplate = """
Below is a prompt template that you need to use for the GitHub documentation:
Project Name
1. Description
A brief overview of what the project does, its purpose, and key features.

2. Classes
	- Class 1
		Attributes
			attribute1 (type): Description of the first attribute.
			attribute2 (type): Description of the second attribute.
		Functions
			function_name(param1: type, param2: type) -> return_type
				Parameters:
					param1 (type): Description of the first parameter.
					param2 (type): Description of the second parameter.
				Returns:
					return_type: Description of the return value.
	- Class 2
"""

testPromptTemplate = """
Please write code and generate comprehensive and accurate test cases 
that cover various scenarios, including edge cases and typical use cases.
Below is a prompt template that you need to use for test cases:
# Description of the test case scenario
# Input: Input values
# Expected Output: Expected output values
Code
"""

# Construct the prompt message
message = """
Here is the code snippet:
from django.db import models
from account.models import Account

# Create your models here.

class PolicySearch(models.Model):
	auto_increment_id   = models.AutoField(primary_key=True)
	created_at          = models.DateTimeField(auto_now_add=True)
	name                = models.CharField(verbose_name="Name", max_length=50)
	keywords 			= models.TextField(verbose_name="Keywords", default="", blank=True)  # Store keywords as a comma-separated string
	account 		    = models.ForeignKey(Account, on_delete=models.CASCADE)
	object_id           = models.CharField(verbose_name="object_id", max_length=50, blank=True)
	progress 	   		= models.IntegerField(default=0, blank=True)
	unique_thread_id 	= models.CharField(blank=True, null=True, max_length=100, default="")
	# no_indicators	 	= models.CharField(blank=True, null=True, max_length=50, default="False")
	


	def __str__(self):
		return self.name + " - " + self.account.email + " - " + str(self.created_at)
	
class OrganisedData(models.Model):
	auto_increment_id   = models.AutoField(primary_key=True)
	created_at          = models.DateTimeField(auto_now_add=True)
	name                = models.CharField(verbose_name="Name", max_length=50)
	object_id           = models.CharField(verbose_name="object_id", max_length=50, blank=True)
	raw_data 		    = models.ForeignKey(PolicySearch, on_delete=models.CASCADE)
	account 		    = models.ForeignKey(Account, on_delete=models.CASCADE)
	# no_indicators	 	= models.CharField(blank=True, null=True, max_length=50, default="False")
	


	def __str__(self):
		return self.name + " - " + self.account.email + " - " + str(self.created_at)
"""

# initiate a chat
user_proxy.initiate_chat(
    assistant,
    message=testPromptTemplate+message,
)