from gui.game import ChessGUI

def main():
	game = ChessGUI()
	while True:
		game.step()

if __name__ == '__main__':
	main()