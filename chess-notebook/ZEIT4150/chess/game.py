
import pdb
import time
import timeit
import random
import chess
import chess.svg
import chess.pgn
import chess.engine

import pickle as pkl
import dill

import numpy as np
import multiprocessing
# multiprocessing.set_start_method('spawn')

from threading import Thread

from collections import deque

from chess.polyglot import zobrist_hash
from copy import deepcopy

from IPython.display import display, HTML, clear_output

import ipywidgets as widgets
from math import log


####


class ChessGame():
    def __init__(self,
                 fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
                 scoreFn=lambda b: 0, vizSize=256,
                 nLogLines=16,
                 nAgentLogLines=4,
                 useSVG=True, pause=0.01, gameInfo=""):
        """

        Credit: Mo Hossny
        AdoptedFrom: https://bit.ly/3qImKaT

        :param fen: 		    FEN string describing starting position on the board
        :param scoreFn: 		Evaluation function of current position on the board
        :param vizSize: 		Board rendering size (square image)
        :param nLogLines:       (DO NOT CHANGE) Number of log lines in the margin
        :param nAgentLogLines:  (DO NOT CHANGE) Number of log line in the agent logging area
        :param useSVG: 		    Whether to visualise the board as SVG (in jupyter like environments)
        :param pause: 		    Delay time for board drawing thread
        :param gameInfo: 	    String to be passed to the game and displayed at the head of the board (jupyter-like environments)

        """
        self.__dict__.update(locals())
        self.vizSize = vizSize
        self.scoreFn = scoreFn
        self.headerInfo = ""
        self.footerInfo = ""

        self.nAgentLogLines = nAgentLogLines
        self.nLogLines = nLogLines
        self.loggerInfo = deque([], nAgentLogLines)
        self.marginInfo = deque([], nLogLines)

        self.gameInfo = ""
        self.evalInfo = ""
        self.moveInfo = ""
        self.moreInfo = ""
        self.matchInfo = ""
        self.pause = pause
        self.useSVG = useSVG
        self.startingFEN = fen

        self.board = chess.Board(fen)
        self.curZHash = str(zobrist_hash(self.board))
        self.curFEN = self.board.fen()

        self.newMove = False
        self.moveArrows = {}
        self.moveBluArrows = []
        self.moveRedArrows = []
        self.moveTintArrows = []

        self.vizdBoard = self.renderBoard(self.board)
        self.whiteUI = widgets.VBox()
        self.blackUI = widgets.VBox()
        self.makeUI()
        self.thVisualiser = None
        return

    def renderBoard(self, board):
        lastMove = board.move_stack[-1] if board.move_stack else None
        self.vizdBoard = chess.svg.board(board,
                                         lastmove=lastMove,
                                         # check=True,
                                         arrows=sum(self.moveArrows.values(), []),
                                         # [*self.moveArrows,
                                         #         *self.moveBluArrows,
                                         #         *self.moveRedArrows,
                                         #         *self.moveTintArrows],
                                         size=self.vizSize)
        return self.vizdBoard

    def toPGN(self, event="Casual Game"):
        """Packs moves played in the game into PGN format.  PGN text
        can be imported into chess.com and lichess.org for further
        analysis.

        :param event: A title for the game (e.g. tournment X ...)

        :returns: PGN text.
        """
        game = chess.pgn.Game()
        game.setup(chess.Board(self.startingFEN))
        game.headers["Event"] = event
        moves = self.board.move_stack

        if not moves:
            return ""

        node = game.add_main_variation(moves[0])
        for mv in moves[1:]:
            node = node.add_main_variation(mv)
            pass

        return f"{game}\n\n"

    def saveGame(self, fileName):
        """Saves the moves into a PGN file.

        :param fileName: Path to PGN file
        :returns: PGN text.

        """
        pgn = self.toPGN()

        print(pgn, file=open(fileName, "w"), end="\n\n")
        return pgn


    def makeUI(self):
        """[INTERNAL] Builds jupyter UI for the chess game using ipywidgets.

        :returns: None

        """
        Layout = widgets.Layout
        loggerInfo = self.loggerInfo.copy()
        marginInfo = self.marginInfo.copy()

        self.vizBoard = self.renderBoard(self.board)

        self.gameText = widgets.HTML(value=f'<p style="color:green">{self.gameInfo}<br/></p>')
        self.evalText = widgets.HTML(value=f'<p style="color:green">{self.evalInfo}<br/></p>')
        self.headerText = widgets.HTML(value=f'<p style="color:green">{self.headerInfo}<br/></p>')
        self.boardImage = widgets.HTML(value=f'{self.vizdBoard}', width="50%")
        self.footerText = widgets.HTML(value=f'<p style="color:green">{self.footerInfo}<br/></p>')
        self.loggerText = widgets.HTML(value='<p style="color:green">' +
                                       "".join([f"{data}"
                                                     for data in loggerInfo]) +
                                       '</p>')



        layout = widgets.Layout(width=f"{self.vizSize}px",
                                height=f"{self.vizSize}px")
        self.marginText = widgets.HTML(layout=Layout(width="100%", height="100%"),
                                       value='<p style="color:green">' +
                                       "".join([f"{data}"
                                                     for data in marginInfo]) +
                                       '</p>')

        self.zhashText = widgets.Text(value="",
                                      #description="Hash",
                                      layout=Layout(width="98%",
                                                    height="24px"))
        self.fenText = widgets.Text(value="",
                                    #description="FEN",
                                    layout=Layout(width="98%",
                                                  height="24px"))
        self.pgnText = widgets.Textarea(value="", layout=Layout(width="98%",
                                                                height="100%"))
        self.pgnBox = widgets.VBox([self.zhashText,
                                    self.fenText,
                                    self.pgnText], layout=Layout(width="100%",
                                                                height="100%"))
        self.notesText = widgets.Textarea(value="", layout=Layout(width="98%",
                                                                  height="100%"))
        self.marginTab = widgets.Tab([self.marginText,
                                      self.pgnBox,
                                      self.notesText
                                     ],
                                    layout=Layout(width="50%", height=f"{self.vizSize}px"))
        self.marginTab.set_title(0, "Msgs")
        self.marginTab.set_title(1, "FEN/PGN")
        self.marginTab.set_title(2, "Notes")

        self.margin = widgets.VBox([#self.gameText,
                                    #self.evalText,
                                    self.marginTab])

        self.vbox = widgets.VBox([#self.gameText,
                                  #self.evalText,
                                  #self.headerText,
                                  self.whiteUI,
                                  self.boardImage,
                                  self.blackUI])
                                  #self.footerText,
                                  #self.loggerText])
        self.board_and_margin = widgets.HBox([self.boardImage, self.marginTab], height="100%")

        self.hbox = widgets.HBox([self.boardImage, self.marginTab])
        self.vbox = widgets.VBox([self.gameText,
                                  self.blackUI,
                                  self.hbox,
                                  self.whiteUI],
                                 layout=Layout(width=f"{2*self.vizSize}px"))
        # clear_output(wait=True)
        display(self.vbox)
        return

    def print(self, *args, **kwargs):
        """[DEPRECATED] A proxy function to capture stdout prints.

        :returns: None

        """
        with self.outputText:
            return print(*args, **kwargs)

    def updateUI(self):
        """[INTERNAL] Updates values in jupyter ipywidgets widgets.

        :returns: None

        """
        loggerInfo = self.loggerInfo.copy()
        marginInfo = self.marginInfo.copy()

        self.vizBoard = self.renderBoard(self.board)

        self.zhashText.value = self.curZHash
        self.fenText.value = self.curFEN

        self.gameText.value = f'<p style="color:green">{self.gameInfo} - Move: {self.board.fullmove_number}<br/></p>'
        self.evalText.value = f'<p style="color:green">{self.evalInfo}<br/></p>'
        self.headerText.value = f'<p style="color:green">{self.headerInfo}<br/></p>'
        self.footerText.value = f'<p style="color:green">{self.footerInfo}<br/></p>'
        self.boardImage.value = f'{self.vizdBoard}'
        self.loggerText.value = ('<p style="color:green">' +
                                 "<br/>".join([f"{data}"
                                               for data in loggerInfo]) +
                                 '</p>')
        self.marginText.value = ('<p style="color:green">' +
                                 "<br/>".join([f"{data}"
                                               for data in marginInfo]) +
                                 '</p>')
        # self.notesText.value = "\n".join([f"{data}"
        #                                        for data in marginInfo])
        self.pgnText.value = self.toPGN()
        return

    def drawBoard(self):
        """[INTERNAL] Drawing function always running in a thread.

        :returns: None

        """
        while self.thVisualiserLive:
            time.sleep(self.pause)

            if self.useSVG:
                board = self.board
                self.updateUI()
                pass
            pass
        return

    def playGame(self, whiteAgent, blackAgent, gameTime=0,
                 nMoves=0,
                 visualise=False):
        """Runs a game between two agents.  It handles
        `KeyboardInterrupt` exception to stop the drawing thread
        before raising the exception.  Other exceptions are captured
        and error messages are logged.

        :param whiteAgent: A callable which accepts a `chess.Board`
            anre returns a `chess.Move`
        :param blackAgent: A callable which accepts a `chess.Board`
            anre returns a `chess.Move`
        :param gameTime: Timer (TODO)
        :param nMoves: Max.  number of moves in the game.  Can be used
            for short term training.
        :param visualise: If `True`, it visualises the board and UI.

        :returns: `chess.Outcome`
        """
        try:
            self.whiteUI = whiteAgent.getUI()
            self.blackUI = blackAgent.getUI()
            if visualise:
                del self.vbox
                clear_output(wait=True)
                self.makeUI()
                # self.vbox.children = [self.gameText,
                #                       self.blackUI,
                #                       self.hbox,
                #                       self.whiteUI]
                # display(self.vbox)
                self.startBoard()
                pass

            while (not nMoves or self.board.fullmove_number < nMoves) and not self.board.is_game_over(claim_draw=True):
                score = self.scoreFn(self.board)
                self.evalInfo = f"{score=: 2.3f}"
                turn = self.board.turn
                self.curZHash = str(zobrist_hash(self.board))
                self.curFEN = self.board.fen()

                agent = whiteAgent if turn else blackAgent
                # agentInfo = self.addFooterInfo if turn else self.addHeaderInfo

                move = agent(self.board.copy(), gameTime,
                             self.highlightBluMoves,
                             self.highlightRedMoves,
                             self.highlightGrnMoves,
                             self.highlightYlwMoves,
                             # agentInfo,
                             # self.addLoggerInfo,
                             self.addMarginInfo)

                self.makeMove(move)

                pass
            outcome = self.board.outcome(claim_draw=True)
            if outcome:
                self.addMarginInfo([repr(outcome),
                                    repr(outcome.termination),
                                    repr(outcome.result())])
                pass
            self.stopBoard()
            pass
        except KeyboardInterrupt:
            self.addMarginInfo(["Interrupted by user!!"])
            self.stopBoard()
            raise
            pass
        except:
            import traceback as tb
            self.addMarginInfo(["Exception raised!!!!"])
            self.addMarginInfo(tb.format_exc().split('\n'))
            self.stopBoard()
            tb.print_exc()
            raise
            pass

        return outcome

    def resetGame(self, fen=None):
        """Resets the board.

        :param fen: FEN string describing board position
        :returns: None

        """
        self.board.set_fen(fen or self.startingFEN)

    def makeMove(self, move):
        """[INTERNAL] Applyes the `move` to the board.

        :param move: A chess move
        :returns: None

        """
        self.board.push(move)
        self.newMove = True

    def startBoard(self):
        """Starts a the board drawing thread.

        :returns: None

        """
        if self.thVisualiser:
            self.addMarginInfo(["Thread is active ... stopping"])
            #self.stopBoard()
            pass

        self.thVisualiser = Thread(target=self.drawBoard,
                                   daemon=True)
        self.thVisualiserLive = True
        self.thVisualiser.start()
        return

    def stopBoard(self):
        """Stops board drawing thread

        :returns:

        """
        self.addMarginInfo(["Stopping thread..."])
        self.thVisualiserLive = False
        time.sleep(.1)
        self.thVisualiser.join()
        self.marginText.value += f"\n\nThread stopped..."
        # print("Thread stopped...")
        return

    def highlightSquares(self, squares):
        """[NOT IMPLEMENTED] Highlightes squares on the board

        :param squares: A `chess.SquareSet`
        :returns: None

        """
        pass

    def prepArrows(self, moves: chess.Move, color="#000000"):
        """[INTERNAL] Prepares arrows for display on the board.
        Arrows have increasing opacity.

        :param moves: Chess moves
        :param color: Web format RGB color (e.g. '#000000') of the arrows

        :returns: A list of `chess.Arrow`
        """
        Arrow = chess.svg.Arrow
        nMoves = len(moves)
        stepOpacity = 255 // (nMoves + 2)
        offsetOpacity = 255 // nMoves
        return [Arrow(mv.from_square,
                      mv.to_square, color=f"{color}{stepOpacity*i+offsetOpacity:02x}")
                for i, mv in enumerate(moves)]

    def highlightMoves(self, moves, color):
        self.moveArrows[color] = self.prepArrows(moves, color)
        return

    def highlightRedMoves(self, moves):
        return self.highlightMoves(moves, color="#cc0000")

    def highlightGrnMoves(self, moves):
        return self.highlightMoves(moves, color="#00cc00")

    def highlightBluMoves(self, moves):
        return self.highlightMoves(moves, color="#0000cc")

    def highlightYlwMoves(self, moves):
        return self.highlightMoves(moves, color="#cccc00")

    def addMarginInfo(self, lines, replace=False):
        if isinstance(lines, str):
            return self.addMarginInfo([lines], replace=replace)

        if not replace:
            self.marginInfo += lines
            self.notesText.value += '\n'.join(lines)
        else:
            self.marginInfo = lines
            self.notesText.value = '\n'.join(lines)
            pass
        return

    def addLoggerInfo(self, lines, replace=False):
        if isinstance(lines, str):
            return self.addLoggerInfo([lines], replace=replace)

        if not replace:
            self.loggerInfo += lines
        else:
            self.loggerInfo = lines

    def addHeaderInfo(self, txt, append=False):
        if append:
            self.headerInfo += txt
        else:
            self.headerInfo = txt

    def addFooterInfo(self, txt, append=False):
        if append:
            self.footerInfo += txt
        else:
            self.footerInfo = txt

    def addGameInfo(self, txt, append=False):
        if append:
            self.gameInfo += txt
        else:
            self.gameInfo = txt

    @property
    def player(self):
        """Player color as string.

        :returns: 'White' or 'Black'

        """
        return "White" if self.board.turn == chess.WHITE else "Black"

    @property
    def move(self):
        """Last move

        :returns: `chess.Move`

        """
        return self.board.move_stack or self.board.move_stack[-1]

    pass
