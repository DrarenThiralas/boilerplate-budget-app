def formatNumber(number):
	amountStr = str(number)
	dotIndex = amountStr.find(".")
	if dotIndex == -1:
		amountStr+=".00"
	else:
		if len(amountStr[dotIndex+1:])==1:
			amountStr+="0"
		else:
			amountStr=amountStr[:dotIndex+3]
	return amountStr

class Category:

	def __init__(self, name):
		self.name = name
		self.ledger = []
		self.balance = 0

	def deposit(self, amount, desc = ""):
		self.ledger.append({"amount":amount, "description":desc})
		self.balance += amount

	def withdraw(self, amount, desc = ""):
		if not self.check_funds(amount):
			return False
		else:
			self.ledger.append({"amount":-amount, "description":desc})
			self.balance -= amount
			return True

	def get_balance(self):
		return self.balance

	def transfer(self, amount, target):
		desc1 = "Transfer from "+self.name
		desc2 = "Transfer to "+target.name
		success = self.withdraw(amount, desc2)
		if success:
			target.deposit(amount, desc1)
		return success

	def check_funds(self, amount):
		return not (amount > self.balance)

	def __str__(self):
		resultString = ""
		for i in range(15-int((len(self.name)+1)/2)):
			resultString+="*"
		resultString+=self.name
		for i in range(15-int(len(self.name)/2)):
			resultString+="*"
		resultString += "\n"



		for item in self.ledger:
			desc = item["description"]
			if len(desc)>23:
				desc = desc[:23]

			amountStr = formatNumber(item["amount"])

			spaceStr = ""
			for i in range(30-len(desc)-len(amountStr)):
				spaceStr+=" "

			resultString += desc + spaceStr + amountStr +"\n"

		resultString += "Total: "+formatNumber(self.balance)


		return resultString




def create_spend_chart(categories):

	spendingsList = [0 for i in range(len(categories))]
	for i in range(len(categories)):
		for entry in categories[i].ledger:
			if entry["amount"]<0:
				spendingsList[i] -= entry["amount"]

	spendingsTotal = sum(spendingsList)
	spendingsList = list(map(lambda x: int(x/spendingsTotal * 10)*10, spendingsList))


	resultString = "Percentage spent by category\n"
	linesNum = 11

	for i in range(linesNum):

		linePerc = (linesNum-i-1)*10
		lineLabel = str(linePerc)+"| "
		while len(lineLabel)<5:
			lineLabel = " "+lineLabel

		resultString += lineLabel

		for j in range(len(categories)):
			if spendingsList[j]>=linePerc:
				resultString+="o  "
			else:
				resultString+="   "

		resultString += "\n"

	lineLength = 5+len(categories)*3
	separatorString = "    "
	for i in range(lineLength-4):
		separatorString+="-"
	resultString+=separatorString+"\n"

	namesList = [category.name for category in categories]
	linesNum = max(list(map(len, namesList)))
	for i in range(linesNum):
		resultString += "     "
		for j in range(len(categories)):
			if i >= len(categories[j].name):
				resultString +=" "
			else:
				resultString += categories[j].name[i]
			resultString += "  "
		resultString += "\n"

	return resultString[:-1]