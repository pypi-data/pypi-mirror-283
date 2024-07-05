__all__=['get_stack_top']
def get_stack_top(frame):
	A=frame
	while True:
		if not A.stack.is_empty():return A.stack.top
		A=A.prev_frame
		if A is None:raise;throw(UELRuntimeError,'Stack is empty');return