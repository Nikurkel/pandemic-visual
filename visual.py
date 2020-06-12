import pygame
import pygame_gui
import random
import sys
import math

pygame.init()

WIDTH = 1600
HEIGHT = 900
surface = pygame.display.set_mode((WIDTH,HEIGHT))

BLACK = (0,0,0)
GREY = (100,100,100)
RED = (200,100,100)
BLUE = (100,150,200)
DARK = (10,10,10)
WHITE = (255,255,255)

emptyColor = (50,50,50)
settingsColor = (30,50,50)

font = pygame.font.SysFont("times new roman", 20)

#define main
def main():
	gui = Gui()
	gui.buildGui()

	while True:
		
		gui.runGui()

#define classes
class Gui:
	def __init__(self):
		self.guiclock = pygame.time.Clock()
		self.manager = pygame_gui.UIManager((WIDTH,HEIGHT))
		self.background = pygame.Surface((WIDTH,HEIGHT))
		self.nextPeopleNumber = 300
		self.sim = Simulation('basic', self.nextPeopleNumber, 10, 140, 5, 1, 0, 0)
		self.simRunning = False
		self.speed = 30 #FPS (0 = max FPS)
		self.counter = 0

	def buildGui(self):
		self.buildStandartGraphics()	

		self.sim.updateSimulation(self.distancingSlider.get_current_value())
		self.sim.saveDay()
		self.sim.course.updateCourse(self.sim.population)

		
	def buildStandartGraphics(self):
		pygame.display.set_caption('GUI')

		pygame.draw.rect( surface, BLACK , (0,0,WIDTH,HEIGHT)) #GUI background
		pygame.draw.rect( surface, emptyColor , (270,70,600,300)) #course background
		pygame.draw.rect( surface, settingsColor , (270,475,600,400)) #options background

		pygame_gui.elements.UILabel(relative_rect=pygame.Rect(1000, 15, 500, 40),text='Simulation',manager=self.manager)
		pygame_gui.elements.UILabel(relative_rect=pygame.Rect(270, 15, 600, 40),text='Course',manager=self.manager)

		#Menu
		pygame_gui.elements.UILabel(relative_rect=pygame.Rect(20, 10, 200, 40),text='Menu',manager=self.manager)

		self.pauseButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(20, 60, 95, 40),text='play',manager=self.manager)
		self.resetButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(125, 60, 95, 40),text='reset',manager=self.manager)
		self.customButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(20, 110, 200, 40),text='basic version',manager=self.manager)

		self.loadMenu = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect(20, 170, 200, 40),options_list=(getSaveNameList()),starting_option="saved files",manager=self.manager)

		self.deleteButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(20, 220, 95, 40),text='delete',manager=self.manager)
		self.loadButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(125, 220, 95, 40),text='load',manager=self.manager)

		self.saveNameEntry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(20, 270, 150, 25),manager=self.manager)
		self.saveButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(180, 270, 40, 25),text='save',manager=self.manager)

		self.peopleLabel = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(20, 320, 200, 25),text='individuals',manager=self.manager)
		self.peopleEntry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(20, 350, 200, 25),manager=self.manager)
		self.peopleEntry.set_text(str(len(self.sim.population)))

		self.customLabel = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(20, 410, 200, 40),text='Custom Settings',manager=self.manager)

		self.livingMenu = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect(20, 460, 200, 40),options_list=("1","2","3","4","5","6"),starting_option="living spaces",manager=self.manager)
		self.quarantineMenu = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect(20, 510, 200, 40),options_list=("0","1"),starting_option="quarantine spaces",manager=self.manager)
		self.meetingMenu = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect(20, 560, 200, 40),options_list=("0","1","2"),starting_option="meeting spaces",manager=self.manager)

		self.tUntilQuarantineLabel = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(15, 620, 210, 25),text='isolate after (0-100%) 50',manager=self.manager)
		self.tUntilQuarantineSlider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect(20, 650, 200, 25),start_value=50,value_range=(0,100),manager=self.manager)

		self.randomTravelLabel = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(20, 700, 200, 25),text='random travel (0-20%) 0',manager=self.manager)
		self.randomTravelSlider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect(20, 730, 200, 25),start_value=0,value_range=(0,20),manager=self.manager)

		self.targetTravelLabel = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(20, 780, 200, 25),text='target travel (0-20%) 5',manager=self.manager)
		self.targetTravelSlider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect(20, 810, 200, 25),start_value=5,value_range=(0,20),manager=self.manager)


		#Options
		pygame_gui.elements.UILabel(relative_rect=pygame.Rect(270, 420, 600, 40),text='Options',manager=self.manager)

		self.speedLabel  = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(280, 500, 300, 25),text='target t/s '+str(str(self.speed)),manager=self.manager)
		self.speedSlider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect(600, 500, 250, 25),start_value=30,value_range=(10,100),manager=self.manager)

		pygame_gui.elements.UILabel(relative_rect=pygame.Rect(280, 550, 300, 25),text='Incubation time (t)',manager=self.manager)
		self.incubationEntry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(600, 550, 250, 25),manager=self.manager)
		self.incubationEntry.set_text(str(self.sim.incubationT))

		pygame_gui.elements.UILabel(relative_rect=pygame.Rect(280, 600, 300, 25),text='Infectious time (t)',manager=self.manager)
		self.infectiousEntry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(600, 600, 250, 25),manager=self.manager)
		self.infectiousEntry.set_text(str(self.sim.infectionT))

		self.infectRadiusLabel = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(280, 650, 300, 25),text='infect radius (5-25px) 5',manager=self.manager)
		self.infectRadiusSlider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect(600, 650, 250, 25),start_value=5,value_range=(5,25),manager=self.manager)

		self.infectionChanceLabel = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(280, 700, 300, 25),text='infection chance (0-100%) 10',manager=self.manager)
		self.infectionChanceSlider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect(600, 700, 250, 25),start_value=10,value_range=(0,100),manager=self.manager)

		self.distancingLabel = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(280, 750, 300, 25),text='distancing willingness (0-100%) 0',manager=self.manager)
		self.distancingSlider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect(600, 750, 250, 25),start_value=0,value_range=(0,100),manager=self.manager)	

		
	def updateBackground(self):
		pygame.draw.rect( surface, settingsColor , (0,0,240,HEIGHT))
		pygame.draw.rect( surface, emptyColor , (238,0,4,HEIGHT)) 
		pygame.draw.rect( surface, emptyColor , (0,398,240,4))
		
	def runGui(self):
		self.updateBackground()
		self.checkInputs()

		if self.simRunning:
		
			self.sim.updateSimulation(self.distancingSlider.get_current_value())

			self.sim.saveDay()

			self.sim.course.updateCourse(self.sim.population)

		self.manager.update(self.guiclock.tick(self.speed))
		self.manager.draw_ui(surface)
		pygame.display.update()

	def checkInputs(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == 27): # window close button + ESCAPE key
				sys.exit()

			if event.type == pygame.USEREVENT:
				if event.user_type == 'ui_button_pressed':
					if event.ui_element == self.pauseButton:
						if self.pauseButton.text == "pause":
							self.pauseButton.set_text("play")
							self.simRunning = False
						else:
							self.pauseButton.set_text("pause")
							self.simRunning = True

					if event.ui_element == self.resetButton:
						
						if self.customButton.text == "basic version":
							self.sim = Simulation('basic', self.nextPeopleNumber, int(self.incubationEntry.text), int(self.infectiousEntry.text), int(self.infectRadiusSlider.get_current_value()),1,0,0)
						
							self.sim.course = Course()
							self.sim.updateSimulation(self.distancingSlider.get_current_value())
							self.sim.saveDay()
							self.sim.course.updateCourse(self.sim.population)

						else:
							if self.livingMenu.selected_option != "living spaces" and self.meetingMenu.selected_option != "meeting spaces" and self.quarantineMenu.selected_option != "quarantine spaces":
								self.sim = Simulation('custom', self.nextPeopleNumber, 10, 140, int(self.infectRadiusSlider.get_current_value()),int(self.livingMenu.selected_option),int(self.quarantineMenu.selected_option),int(self.meetingMenu.selected_option))
							
								self.sim.course = Course()
								self.sim.updateSimulation(self.distancingSlider.get_current_value())
								self.sim.saveDay()
								self.sim.course.updateCourse(self.sim.population)
							
					if event.ui_element == self.customButton:
						if self.customButton.text == "basic version":
							self.customButton.set_text("custom version")
						else:
							self.customButton.set_text("basic version")

					if event.ui_element == self.loadButton:
						defaultSettings = ['Standard', '300', '2', '1', '1', '10', '10', '10', '100', '10', '140', '10', '15', '5' ]
						try:
							myFile = open('savedSettings','r')
							for line in myFile:
								parts = line.split(' ')

								if str(self.loadMenu.selected_option) == 'Standard':
									self.loadSettings(defaultSettings)
								elif str(self.loadMenu.selected_option) == parts[0]:
									self.loadSettings(parts)

						except:
							self.loadSettings(defaultSettings)
							print("save File Fail")
						

					if event.ui_element == self.saveButton:
						self.saveSettings(self.saveNameEntry.text)
					if event.ui_element == self.deleteButton:
						self.deleteSettings(self.loadMenu.selected_option)

			self.manager.process_events(event)

		#update simulation values
		self.speedLabel.set_text('target t/s '+str(self.speed))
		self.speed = int(self.speedSlider.get_current_value())

		self.infectionChanceLabel.set_text("infection chance (0-100%) " + str(int(self.infectionChanceSlider.get_current_value())))
		self.sim.infectionChance = int(self.infectionChanceSlider.get_current_value())

		self.randomTravelLabel.set_text("random travel (0-20%)  " + str(int(self.randomTravelSlider.get_current_value())))
		self.sim.randomTravelChance = int(self.randomTravelSlider.get_current_value())

		self.targetTravelLabel.set_text("target travel (0-20%) " + str(int(self.targetTravelSlider.get_current_value())))
		self.sim.targetTravelChance = int(self.targetTravelSlider.get_current_value())

		self.tUntilQuarantineLabel.set_text("isolate after (0-100%) " + str(int(self.tUntilQuarantineSlider.get_current_value())))
		self.sim.timeUntilQuarantine = self.sim.incubationT + int(self.sim.infectionT*self.tUntilQuarantineSlider.get_current_value()/100)

		self.infectRadiusLabel.set_text("infect radius (5-25px) " + str(int(self.infectRadiusSlider.get_current_value())))

		self.distancingLabel.set_text("distancing willingness (0-100%) " + str(int(self.distancingSlider.get_current_value())))


		if self.speed == 100:
			self.speed = 0
			self.speedLabel.set_text('target t/s Max')

		try:
			self.sim.incubationT = int(self.incubationEntry.text)
		except Exception as e:
			pass
		try:
			self.sim.infectionT = int(self.infectiousEntry.text)
		except Exception as e:
			pass
		try:
			self.nextPeopleNumber = int(self.peopleEntry.text)
		except Exception as e:
			pass

		#update people Size while pause
		if self.sim.population[0].contactradius != self.infectRadiusSlider:
			pygame.draw.rect( surface, DARK , (1000,70,500,500))
			for person in self.sim.population:
				person.change_radius(int(self.infectRadiusSlider.get_current_value()))

				if person.status == "susceptible":
					person.draw(BLUE)
				if person.status == "infected" or person.status == "incubated":
					person.draw(RED)
				if person.status == "removed":
					person.draw(GREY)

	def loadSettings(self, parts):
		print(len(parts))
		print(parts)
		if parts[0] == str(self.loadMenu.selected_option) or parts[0] == 'Standard':

			if len(parts) >= 2:
				self.peopleEntry.text = parts[1]
				self.peopleEntry.redraw()

			if len(parts) >= 3:
				self.livingMenu.kill()
				self.livingMenu = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect(20, 460, 200, 40),options_list=("1","2","3","4","5","6"),starting_option=str(parts[2]),manager=self.manager)
			
			if len(parts) >= 4:
				self.quarantineMenu.kill()
				self.quarantineMenu = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect(20, 510, 200, 40),options_list=("0","1"),starting_option=str(parts[3]),manager=self.manager)
			
			if len(parts) >= 5:
				self.meetingMenu.kill()
				self.meetingMenu = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect(20, 560, 200, 40),options_list=("0","1","2"),starting_option=str(parts[4]),manager=self.manager)

			if len(parts) >= 6:
				self.tUntilQuarantineSlider.set_current_value(int(parts[5]))

			if len(parts) >= 7:
				self.randomTravelSlider.set_current_value(int(parts[6]))

			if len(parts) >= 8:
				self.targetTravelSlider.set_current_value(int(parts[7]))

			if len(parts) >= 9:
				self.speedSlider.set_current_value(int(parts[8]))

			if len(parts) >= 10:
				self.incubationEntry.text = parts[9]
				self.incubationEntry.redraw()

			if len(parts) >= 11:
				self.infectiousEntry.text = parts[10]
				self.infectiousEntry.redraw()

			if len(parts) >= 12:
				self.infectRadiusSlider.set_current_value(int(parts[11]))

			if len(parts) >= 13:
				self.infectionChanceSlider.set_current_value(int(parts[12]))

			if len(parts) >= 14:
				self.distancingSlider.set_current_value(int(parts[13]))

	def saveSettings(self, name):

		settings = []
		settings.append(name)
		settings.append(self.peopleEntry.text)
		settings.append(self.livingMenu.selected_option)
		settings.append(self.quarantineMenu.selected_option)
		settings.append(self.meetingMenu.selected_option)
		settings.append(int(self.tUntilQuarantineSlider.get_current_value()))
		settings.append(int(self.randomTravelSlider.get_current_value()))
		settings.append(int(self.targetTravelSlider.get_current_value()))
		settings.append(int(self.speedSlider.get_current_value()))
		settings.append(self.incubationEntry.text)
		settings.append(self.infectiousEntry.text)
		settings.append(int(self.infectRadiusSlider.get_current_value()))
		settings.append(int(self.infectionChanceSlider.get_current_value()))
		settings.append(int(self.distancingSlider.get_current_value()))

		string = ""
		for i in settings:
			string += str(i)+" "
		string += "\n"

		with open('savedSettings','a') as myFile:
			myFile.write(string)

		self.loadMenu.kill()
		self.loadMenu = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect(20, 170, 200, 40),options_list=(getSaveNameList()),starting_option="saved files",manager=self.manager)



	def deleteSettings(self, name):
		with open("savedSettings", "r") as f:
		    lines = f.readlines()
		with open("savedSettings", "w") as f:
			for line in lines:
				parts = line.split(' ')
				if parts[0] != name:
				    f.write(line)
		self.loadMenu.kill()
		self.loadMenu = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect(20, 170, 200, 40),options_list=(getSaveNameList()),starting_option="saved files",manager=self.manager)


class Simulation:
	def __init__(self, scenario, people, incubationT, infectionT, infectRadius, livingRooms, quarantineRoom, meetingRooms):
		self.course = Course()
		self.people = people
		self.running = False
		self.speed = 1
		self.infectRadius = infectRadius
		self.scenario = scenario
		self.livingRooms = livingRooms
		self.quarantineRoom = quarantineRoom
		self.meetingRooms = meetingRooms
		self.rooms = []
		self.runSim()
		self.incubationT = incubationT
		self.infectionT = infectionT
		self.infectionChance = 10
		self.timeUntilQuarantine = 50
		self.randomTravelChance = 0
		self.targetTravelChance = 0
		self.population[0].status = "incubated"
		self.population[0].update(self.incubationT, self.infectionT)
		print(self.incubationT)

	def runSim(self):
		if  (self.scenario == 'basic'):
			self.rooms.append(Room(1000,70,500,500,"living"))
			self.population = [Person(self.infectRadius,self.rooms[0]) for _ in range(self.people)]
			
		elif(self.scenario == 'custom'):
			self.rooms.append(Room(1000,70,500,500,"travelLayer"))
			if self.livingRooms > 0:
				if self.livingRooms == 1:
					self.rooms.append(Room(1010,80,480,315,"living"))
					self.population = ([Person(self.infectRadius,self.rooms[-1]) for _ in range(int(self.people/self.livingRooms))])
				else:
					self.rooms.append(Room(1010,80,150,150,"living"))
					self.population = ([Person(self.infectRadius,self.rooms[-1]) for _ in range(int(self.people/self.livingRooms))])
			if self.livingRooms > 1:
				self.rooms.append(Room(1175,80,150,150,"living"))
				self.population += ([Person(self.infectRadius,self.rooms[-1]) for _ in range(int(self.people/self.livingRooms))])
			if self.livingRooms > 2:
				self.rooms.append(Room(1340,80,150,150,"living"))
				self.population += ([Person(self.infectRadius,self.rooms[-1]) for _ in range(int(self.people/self.livingRooms))])
			if self.livingRooms > 3:
				self.rooms.append(Room(1010,245,150,150,"living"))
				self.population += ([Person(self.infectRadius,self.rooms[-1]) for _ in range(int(self.people/self.livingRooms))])
			if self.livingRooms > 4:
				self.rooms.append(Room(1175,245,150,150,"living"))
				self.population += ([Person(self.infectRadius,self.rooms[-1]) for _ in range(int(self.people/self.livingRooms))])
			if self.livingRooms > 5:
				self.rooms.append(Room(1340,245,150,150,"living"))
				self.population += ([Person(self.infectRadius,self.rooms[-1]) for _ in range(int(self.people/self.livingRooms))])
			if self.quarantineRoom == 1:
				self.rooms.append(Room(1175,410,150,150,"quarantine"))
			if self.meetingRooms > 0:
				self.rooms.append(Room(1010,410,150,150,"meeting"))
			if self.meetingRooms > 1:
				self.rooms.append(Room(1340,410,150,150,"meeting"))
				

	def updateSimulation(self, distancingChance):
		pygame.draw.rect( surface, DARK , (1000,70,500,500)) #simulation background

		for r in self.rooms:
			r.draw()

		susceptiblePeople = self.getSusceptiblePeople()
		for person in self.population:
			try:
				self.distancing(person, distancingChance)# move
			except Exception as e:
				pass
			person.update(self.incubationT, self.infectionT)

			if person.status == "infected" and len(susceptiblePeople) > 0:
				person.infect(susceptiblePeople, self.infectionChance)

			if self.quarantineRoom > 0:
				if person.days > self.timeUntilQuarantine and person.days < self.infectionT + 50 and person.room.function != "quarantine":
					for r in self.rooms:
						if r.function == "quarantine":
							person.travel(r)

			if person.days > self.infectionT + 100 and person.room.function == "quarantine":
				person.travel(person.orgRoom)

			if self.livingRooms > 1 and person.room.function == "living":
				if self.randomTravelChance > random.randint(0,99):
					person.travel(self.rooms[random.randint(1,self.livingRooms)])

			if self.meetingRooms > 0:
				print(self.targetTravelChance)
				if person.room.function == "living" and self.targetTravelChance > random.randint(0,99):
					person.travel(self.rooms[-(random.randint(1,self.meetingRooms))])
				if person.room.function == "meeting"and 20 > random.randint(0,99): # hardcoded probability ####
					person.travel(person.orgRoom) 

	def getSusceptiblePeople(self):
			susceptible = []
			for nearby in self.population:
				if nearby.status == "susceptible":
					susceptible.append(nearby)
			return susceptible

	def distancing(self, person, distancingChance):
		if random.randint(1,99) < distancingChance:

			nearest = self.population[0]
			if nearest == person:
				nearest = self.population[1]

			minDistance = 1000
			for nearby in self.population:
				if person != nearby and person.room == nearby.room:
					dx = person.x - nearby.x
					dy = person.y - nearby.y
					distance = math.sqrt( dx * dx + dy * dy )
					if distance < minDistance:
						minDistance = distance
						nearest = nearby

			if nearest.x > person.x:
				east = False
			else:
				east = True
			if nearest.y > person.y:
				north = True
			else:
				north = False
			try:
				person.move2(north,east)
			except:
				person.days += 1
			
		else:
			try:
				person.move1()
			except:
				person.days += 1

	def getBigR(self):
		g1 = 0 #group 1
		g2 = 0 #group 2
		for person in self.population:
			if person.days > 0 and person.days < self.infectionT/2:
				g1 += 1
			if person.days > self.infectionT/2 and person.days < self.infectionT:
				g2 += 1
		if g1 > 0 and g2 > 0:
			return g1 / g2
		else:
			return 0

	def saveDay(self):
		r = 0 #removed
		s = 0 #susceptible
		i = 0 #infectious
		for person in self.population:
			if person.status == "susceptible" or person.status == "incubated":
				s+= 1
			if person.status == "infected":
				i+= 1
			if person.status == "removed":
				r+= 1
		bigR = self.getBigR()

		self.course.newDay(r,s,i,bigR)

		#doubling time
		if bigR > 1:
			doubleTime = self.course.getDoubleTime()
		else:
			doubleTime = 0

		newCases = self.course.getNewCases()

		maxR = 0
		addR = 0
		countR = 0
		avgR = 0
		for d in self.course.days:
			if d.R > maxR:
				maxR = d.R
			if d.R > 0:
				countR += 1
				addR += d.R
		if bigR > maxR:
			maxR = bigR
		try:
			avgR = addR / countR
		except:
			pass
		

		self.draw_stats(r,s,i,bigR,avgR,maxR,doubleTime,newCases)

	def draw_stats(self,r,s,i,bigR,avgR,maxR,dt,newCases):
		pygame.draw.rect( surface, BLACK , (1000,600,600,300)) #course desc grey

		pygame.draw.rect( surface, GREY , (1000,600,20,20)) #course desc grey
		self.write(str("Removed: " + str(int(r))),1025,600)

		pygame.draw.rect( surface, BLUE , (1160,600,20,20)) #course desc blue
		self.write(str("Susceptible: " + str(int(s))),1185,600)

		pygame.draw.rect( surface, RED , (1350,600,20,20)) #course desc red
		self.write(str("Infectious: " + str(int(i))),1375,600)
		

		self.write(str("R = " + str(round(bigR, 2))),1000,650)
		self.write(str("avg(R) = " + str(round(avgR, 2))),1000,690)
		self.write(str("max(R) = " + str(round(maxR, 2))),1000,730)
		self.write(str("t = " + str(len(self.course.days))),1000,770)
		self.write(str("doubleTime = " + str(dt)),1000,810)
		self.write(str("new Cases = " + str(newCases)),1000,850)

		self.write("R = group1(0 - 1/2 infT) / group2(1/2 - 1 infT)",1200,650)
		self.write("avg(R) = ( R(t1) + ... ) / count(R)  || R(x) > 0",1200,690)
		self.write("biggest R",1200,730)
		self.write("time units",1200,770)
		self.write("dT = t2(cases) - t1(cases/2) || R(now) > 1",1200,810)
		self.write("new Cases in last 20t",1200,850)

		# course x-achsis
		oneFourth = len(self.course.days)/4
		pygame.draw.rect( surface, BLACK , (250,370,700,40)) #remove old numbers

		pygame.draw.rect( surface, BLACK , (880,360,20,20))
		self.write("t",880,360)

		pygame.draw.rect( surface, WHITE , (270,370,2,5)) #number 1
		self.write(str(0),265,380)

		pygame.draw.rect( surface, WHITE , (420,370,2,5)) #number 2
		self.write(str(round(oneFourth)),410,380)

		pygame.draw.rect( surface, WHITE , (570,370,2,5)) #number 3
		self.write(str(round(oneFourth*2)),560,380)

		pygame.draw.rect( surface, WHITE , (720,370,2,5)) #number 4
		self.write(str(round(oneFourth*3)),710,380)

		pygame.draw.rect( surface, WHITE , (868,370,2,5)) #number 5
		self.write(str(round(oneFourth*4)),858,380)

	def write(self, txt, x, y):
		removedTxt = font.render(txt, True, (200, 200, 200))
		surface.blit(removedTxt,(x,y))

class Room:
	def __init__(self,x,y,width,height,function):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.function = function

	def draw(self):
		pygame.draw.rect( surface, WHITE , (self.x-2,self.y-2,self.width+4,self.height+4)) #simulation lines
		pygame.draw.rect( surface, DARK , (self.x,self.y,self.width,self.height)) #simulation background

class Person:
	def __init__(self,radius,room):
		self.contactradius = radius
		self.minX = room.x + self.contactradius
		self.maxX = (room.x + room.width) - self.contactradius
		self.minY = room.y + self.contactradius
		self.maxY = (room.y + room.height) - self.contactradius
		self.bminX = room.x
		self.bmaxX = (room.x + room.width)
		self.bminY = room.y
		self.bmaxY = (room.y + room.height)
		self.infected = 0
		self.status = "susceptible"
		self.x = random.randint(self.minX,self.maxX)
		self.y = random.randint(self.minY,self.maxY)
		self.speed = 0
		self.days = 0
		self.direction = (0,0)
		self.change_direction(100)
		self.orgRoom = room
		self.room = room

	def change_radius(self,radius):
		if self.status == "infected":
			self.contactradius = radius
		else:
			self.contactradius = 5
		self.minX = self.bminX + self.contactradius
		self.minY = self.bminY + self.contactradius
		self.maxX = self.bmaxX - self.contactradius
		self.maxY = self.bmaxY - self.contactradius

		if(self.y > self.maxY):
			self.y -= radius

		if(self.x > self.maxX):
			self.x -= radius

		if(self.y < self.minY):
			self.y += radius

		if(self.x < self.minX):
			self.x += radius

	def change_direction(self, prob):
		if random.randint(0, 99) < prob:
			self.direction = (random.randint(-2,2), random.randint(-2,2))
		
	def move1(self):

		self.x += self.direction[0]
		self.y += self.direction[1]

		if(self.y > self.maxY):
			self.y -= int(math.sqrt(self.direction[1]*self.direction[1]))

		if(self.x > self.maxX):
			self.x -= int(math.sqrt(self.direction[0]*self.direction[0]))

		if(self.x < self.minX):
			self.x += int(math.sqrt(self.direction[0]*self.direction[0]))

		if(self.y < self.minY ):
			self.y += int(math.sqrt(self.direction[1]*self.direction[1]))
		
		self.change_direction(5)

	def move2(self,north,east):

		self.direction = (int(math.sqrt(self.direction[0]*self.direction[0])),int(math.sqrt(self.direction[1]*self.direction[1])))# makes sure direction is positive

		if north:
			self.y -= self.direction[1]
		else:
			self.y += self.direction[1]
		if east:
			self.x += self.direction[0]
		else:
			self.x -= self.direction[0]

		if(self.y > self.maxY):
			#self.y -= self.direction[1]
			self.y = self.maxY

		if(self.x > self.maxX):
			self.x = self.maxX

		if(self.x < self.minX):
			self.x = self.minX

		if(self.y < self.minY ):
			self.y = self.minY
			
		self.change_direction(100)

	def travel(self,room):
		self.room = room
		self.minX = room.x + self.contactradius
		self.maxX = (room.x + room.width) - self.contactradius
		self.minY = room.y + self.contactradius
		self.maxY = (room.y + room.height) - self.contactradius
		self.bminX = room.x
		self.bmaxX = (room.x + room.width)
		self.bminY = room.y
		self.bmaxY = (room.y + room.height)
		self.x = random.randint(self.minX,self.maxX)
		self.y = random.randint(self.minY,self.maxY)

	def infect(self, group, infectionChance):

		for nearby in group:
			if nearby.status == "susceptible":
				dx = self.x - nearby.x
				dy = self.y - nearby.y
				distance = math.sqrt( dx * dx + dy * dy )


				if(distance < self.contactradius):
					if(random.randint(0,99) < infectionChance): # infection chance
						nearby.status = "incubated"
						self.infected += 1

	def draw(self, color):
		if self.status == "infected":
			pygame.draw.ellipse( surface, color, (self.x-self.contactradius, self.y-self.contactradius, self.contactradius*2, self.contactradius*2),  1)
		pygame.draw.circle( surface, color, (self.x, self.y),  2)

	def update(self,incubationT, infectionT):
		if self.status != "susceptible":
			self.days += 1

		if self.status == "incubated" and self.days > incubationT: # incubated -> infected
			self.status = "infected"
		if self.status == "infected" and self.days > infectionT: # infected -> removed
			self.status = "removed"

		if self.status == "susceptible":
			self.draw(BLUE)
		if self.status == "infected" or self.status == "incubated":
			self.draw(RED)
		if self.status == "removed":
			self.draw(GREY)

class Course:

	def __init__(self):
		self.days = []

	def newDay(self, r, s, i, R):
		self.days.append(Day(r,s,i,R))

	def updateCourse(self, population):
		pygame.draw.rect(surface, BLUE, (270, 70, 600, 300))

		if len(self.days) > 0:
			x = 270.0
			oldX = x-1
			caseRatio = 300 / len(population)
			dayRatio = math.ceil(600/len(self.days))

			#calc graph
			for day in self.days:
				if int(x) > int(oldX):
					rRel = math.ceil(day.r * caseRatio)
					if rRel > 0:
						pygame.draw.rect(surface, GREY, (int(x), 70, dayRatio, rRel))

					iRel = math.ceil(day.i * caseRatio)
					if iRel > 0:
						pygame.draw.rect(surface, RED, (int(x), 370-iRel, dayRatio, iRel))

				oldX = x
				x += 600/len(self.days)

	def getNewCases(self):
		x = len(self.days)-1
		today = self.days[x].i + self.days[x].r
		try:
			yesterday = self.days[x-20].i + self.days[x-20].r
		except Exception as e:
			yesterday = 0
		
		return today - yesterday

	def getDoubleTime(self):
		x = len(self.days)-1

		try:
			while(self.days[x].i > self.days[len(self.days)-1].i / 2):
				x -= 1
			return len(self.days) - x
		except Exception as e:
			return 0
	
class Day():
	def __init__(self, r, s, i, R):
		self.r = r
		self.s = s
		self.i = i
		self.R = R




def getSaveNameList():
	try:
		myFile = open('savedSettings','r')
		saveNames = ['Standard']
		for line in myFile:
			parts = line.split(' ')
			if len(parts) > 0:
				saveNames.append(parts[0])
		return saveNames
	except Exception as e:
		print(e)
		print("File not loaded")
		return {"Standard"}

#call main
main()