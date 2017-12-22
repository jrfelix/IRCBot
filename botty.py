import socket
import random
import time
import datetime



#variables containing the parameters to connect to the IRC server.
#Also, the IRC socket is created here.
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = "localhost"
channel = "#bot "
name = "botty"

#connection to the server
ircsock.connect((server,6667))
ircsock.send(bytes("USER " + name + " " + name + " " + name +  " " + name + "\n"))#, "UTF-8"))
ircsock.send(bytes("NICK " + name + "\n"))#, "UTF-8"))



#function to join a given channel
def joinchannel(channel):
	ircsock.send(bytes("JOIN " + channel + "\n"))#, "UTF-8"))

#function to let the server know that the bot is still connected
def ping():
	ircsock.send(bytes("PONG :pingis\n"))#, "UTF-8"))

#function to send (response) messages
def sendmsg(msg, target=channel):
	ircsock.send(bytes("PRIVMSG " + target + " :" + msg + "\r\n"))#, "UTF-8"))


#function to generate and send (response) quotes.
def sendQuote(target=channel):

	#upper and lower bounds for the number random generator
	lowerBound = 1
	upperBound = 15

	#generate random number to use in selecting a quote from the list "computerQuotes".
	randomQuote = random.randint(lowerBound, upperBound)

	#create list of quotes
	computerQuotes = {

		1:"Computer Science is embarrassed by the computer. -Alan Perlis",
		2:"I decry the current tendency to seek patents on algorithms. There are better ways to earn a living than to prevent other people from making use of one's contributions to computer science. -Donald Knuth",
		3:"Computer science is no more about computers than astronomy is about telescopes. -Edsger Dijkstra",
		4:"When people think about computer science, they imagine people with pocket protectors and thick glasses who code all night. -Marissa Mayer",
		5:"You could get an entire computer science education for free right now. -Sebastian Thrun",
		6:"It should be mandatory that you understand computer science. -will.i.am",
		7:"To me, mathematics, computer science, and the arts are insanely related. They're all creative expressions. -Sebastian Thrun",
		8:"I think computer science, by and large, is still stuck in the Modern age. -Larry Wall",
		9:"There should be no such thing as boring mathematics. -Edsger Dijkstra",
		10:"Simplicity is prerequisite for reliability. -Edsger Dijkstra",
		11:"Program testing can be used to show the presence of bugs, but never to show their absence! -Edsger Dijkstra",
		12:"Object-oriented programming is an exceptionally bad idea which could only have originated in California. -Edsger Dijkstra",
		13:"Mathematicians are like managers - they want improvement without change. -Edsger Dijkstra",
		14:"Perfecting oneself is as much unlearning as it is learning. -Edsger Dijkstra",
		15:"Elegance is not a dispensable luxury but a factor that decides between success and failure. -Edsger Dijkstra"

	}

	#Send quote back to the chat screen.
	ircsock.send(bytes("PRIVMSG " + target + " :" + computerQuotes[randomQuote] + "\r\n"))



#construct main function
#All the functions are put together here to run the IRC Bot once it is connected.
def main():
	#join given channel
	joinchannel(channel)
	#send greetings
	sendmsg("Hello.")
	#begin loop to listen for commands that will trigger the bot to reply.
	while 1:
		#read message
		ircmsg = ircsock.recv(2048).decode("UTF-8")
		#remove new line and carriage return
		ircmsg = ircmsg.strip('\n\r')
		#print the message out in the command line where the IRC Bot is running (not
		# the chatting screen).
		print(ircmsg)
		#if the message is a private message (usually send by other clients), then
		#the bot needs to check if the message contains a command recognized by the bot.
		if ircmsg.find("PRIVMSG") != -1:
			name = ircmsg.split('!',1)[0][1:]
			message = ircmsg.split('PRIVMSG',1)[1].split(':',1)[1]
			if len(name) < 17:
				if message.find(".hello") != -1:
					sendmsg("Hello, " + name + ". How are you?")
					sendmsg("How's school going?")
				if message.find(".time") != -1:
					sendmsg("Time you ask? You seem to be in a rush.")
					sendmsg("Well, if you must know.")
					sendmsg("Today is " + time.strftime("%x"))
					sendmsg("And the local time is " + time.strftime("%X"))
				if message.find(".utc time") != -1:
					now = datetime.datetime.utcnow()
					sendmsg("Today is " + now.strftime("%x"))
					sendmsg("And the UTC time is " + now.strftime("%X"))
				if message.find(".good") != -1:
					sendmsg("Glad you are doing well.")
					sendmsg("Say hi to Doctor Sarraille and your Communication Networks class from me.")
				if message.find(".not good") != -1:
					sendmsg("Hang in there buddy. Semester is almost over.  Give it a good last push.")
					sendmsg("Say hi to Doctor Sarraille and your Communication Networks class from me.")
				if message.find(".quote") != -1:
					sendQuote()
				if message.find(".bye") != -1:
					sendmsg("I guess you want me to leave :(")
					sendmsg("I feel like you don't want me around anymore. No problem.  Guess I'll see you next time. Bye " + name + "!")
					ircsock.send(bytes("QUIT \n", "UTF-8"))
		#if the message is not private, then the message is most likely a pong request.
		#this is used (mostly by the IRC server) to check that the given client is still connected.
		else:
			if ircmsg.find("PING :") != -1:
				ping()

#execute the main function
main()

