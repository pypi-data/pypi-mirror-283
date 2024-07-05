__all__=['UELBaseException']
class UELBaseException:
	def __init__(A,error_message):A.error_message=error_message
	def __str__(A):return f"{A.__class__.__name__}:{A.error_message}"