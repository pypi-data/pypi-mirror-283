


def check_1 ():
	print ("check 1")
	
def check_2 ():
	print ("check 2")
	
def check_3 ():
	raise Exception ("not 110%")

checks = {
	"check 1": check_1,
	"check 2": check_2,
	"check 3": check_3
}