from autogen import AssistantAgent, UserProxyAgent

llm_config = {
  "model": "codellama", 
  "base_url": "http://localhost:11434/v1",
  "api_key": "ollama",
}
assistant = AssistantAgent(
  name="assistant",
  system_message="You are a documentation generator for Python programs",
  llm_config=llm_config
) # the assistant agent

user_proxy = UserProxyAgent(
  name="user_proxy", 
  code_execution_config=False
)

# Construct the prompt message
message = """
Please provide documentation for this code snippet:
from django.db import models
from account.models import Account

# Create your models here.

class PolicySearch(models.Model):
	auto_increment_id = models.AutoField(primary_key=True)
	created_at = models.DateTimeField(auto_now_add=True)
	name = models.CharField(verbose_name="Name", max_length=50)
	keywords = models.TextField(verbose_name="Keywords", default="", blank=True)  # Store keywords as a comma-separated string
	account = models.ForeignKey(Account, on_delete=models.CASCADE)
	object_id = models.CharField(verbose_name="object_id", max_length=50, blank=True)
	progress = models.IntegerField(default=0, blank=True)
	unique_thread_id = models.CharField(blank=True, null=True, max_length=100, default="")
	# no_indicators = models.CharField(blank=True, null=True, max_length=50, default="False")
	
	def __str__(self):
		return self.name + " - " + self.account.email + " - " + str(self.created_at)
"""
# initiate a chat
user_proxy.initiate_chat(
    assistant,
    message=message,
)