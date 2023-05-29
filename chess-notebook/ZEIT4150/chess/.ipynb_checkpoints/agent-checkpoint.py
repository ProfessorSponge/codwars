
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


class ChessAgent:
    def __init__(self, name="Agent",
                 scoreFn=lambda b: 0,
                 dtime=.01,
                 nLogLines=5,
                 train=False):
        """It encapsulates functionalities to communicate with the
        board.  The agent is callable via the `__call__` method which
        recieves a board and function pointers to log and draw
        information on the board.  The agent hosts a UI for
        jupyter-like IDEs which is then called by the board via the
        `getUI` method.

        :param name: Agent name
        :param scoreFn: Scoring function for the agent's decision
            making
        :param dtime: Delay time before move is committed.  Helpful in
            visualisation for very fast agents.
        :param nLogLines: Number of log lines for the agent UI.
        :param train: A flag to determine if the agent is training or
            playing.  Training is much slower.

        :returns: None
        """
        self.__dict__.update(locals())
        self.states = dict()
        self._log2margin = lambda *_: None
        self.loggerInfo = deque([]*nLogLines, nLogLines)
        self.notesInfo = ""
        self.vizdBoards = {}
        self.agentUI = self.makeUI()

        self.log2Agent(f"Agent {self.name} initialised")
        self.log2Agent(f"Ready for action!!")

        return

    def renderSquares(self, squares, color="#0000aa77"):
        self.vizdBoard = chess.svg.board(None,
                                         fill=dict.fromkeys(squares, color),
                                         squares=squares,
                                         size=104)
        return self.vizdBoard

    def renderBoard(self, board, sqcolor="#0000aa77"):
        if isinstance(board, chess.SquareSet):
            return self.renderSquares(board, sqcolor)

        lastMove = board.move_stack[-1] if board.move_stack else None 
        self.vizdBoard = chess.svg.board(board,
                                         lastmove=lastMove,
                                         size=103)
        return self.vizdBoard

    def getUI(self):
        self.uiNotesText.value = ""
        return self.agentUI

    def addLoggerInfo(self, lines, replace=False):
        if isinstance(lines, str):
            return self.addLoggerInfo([lines], replace=replace)

        if not replace:
            self.loggerInfo += lines
        else:
            self.loggerInfo = lines

    def makeUI(self, width="256px"):
        Layout = widgets.Layout
        loggerInfo = self.loggerInfo.copy()
        
        emptyBoard = chess.Board(fen=None)
        vizdBoard = self.renderBoard(emptyBoard)
        
        layout = widgets.Layout(width=width, height="64px")
        self.uiLoggerText = widgets.HTML(width="100%",
                                         value="")
        self.uiNotesText = widgets.Textarea(layout=Layout(width="100%", height="97%"), 
                                            value="")
        self.uiBoardImage = widgets.HTML(value=f'{vizdBoard}')
        self.uiBoards = widgets.HBox([])

        self.uiTab = widgets.Tab(layout=Layout(height="202px"),
                                 children=[self.uiLoggerText, 
                                           self.uiBoards, 
                                           self.uiNotesText])

        self.uiTab.set_title(0, "Msgs")
        self.uiTab.set_title(1, "Boards")
        self.uiTab.set_title(2, "Notes")
        return widgets.VBox([self.uiTab])
        # return widgets.VBox([self.uiLoggerText])

    def drawBoard(self, board, title=""):
        VBox = widgets.VBox
        HTML = widgets.HTML
        image = self.renderBoard(board)
        
        if title not in self.vizdBoards:
            self.vizdBoards[title] = HTML(f"<p><center>{title}</center></p><p><center>{image}</center></p>")
        else:
            self.vizdBoards[title].value = f"<p><center>{title}</center></p><p><center>{image}</center></p>"
            pass

        self.uiBoards.children = list(self.vizdBoards.values())

    def saveStates(self, fileName):
        """Saves the agent learned/explored states to a file
        `filename`.  Uses `dill` for pickling.
        """
        with open(fileName, 'wb') as fp:
            dill.dump(self.states, fp)

    def loadStates(self, fileName):
        """Loads learned/explored states from a file.  Uses `dill` for
        pickling.
        """
        with open(fileName, 'rb') as fp:
            self.states = dill.load(fp)

    def getAction(self, board):
        """[NOTIMPLEMENTED] This is where the magic takes place.  We
        use the `board` supplied by the game to analyse the position
        and return the best move .

        :param board: `chess.Board`

        :returns: `chess.Move`
        """
        raise NotImplementedError
        return
    
    def log2Agent(self, msg, color='green'):
        self.loggerInfo.append((msg, color))
        self.uiLoggerText.value = f"".join([f'<p style="color:{clr}">{txt}</p>'
                                            for txt, clr in self.loggerInfo])

        # self.notesInfo += f"{msg}\n"
        self.uiNotesText.value += f"{msg}\n"

        return

    def log2Margin(self, msg):
        return self._log2margin(f"{self.name}: {msg}")

    def log2Logger(self, msgs):
        return self._log2logger(msgs)

    def drawMyMoves(self, moves):
        return self._drawMyMoves(moves)

    def drawOpponentMoves(self, moves):
        return self._drawOpponentMoves(moves)

    def drawOtherMoves(self, moves):
        return self._drawOtherMoves(moves)

    def drawMoves(self, moves, color):
        return self._drawMoves(moves, color)

    def __call__(self, board, time,
                 _drawMyMoves, _drawOpponentMoves,
                 _drawOtherMoves, _drawMoves,
                 _log2margin):
        self.__dict__.update(locals())
        return self.getAction(board)
    pass


    
