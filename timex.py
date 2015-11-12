import time


x = time.time()
y = time.time()
print x
print "Frozen for 5 seconds starting now."
while y < x + 5:
	y = time.time()
print y