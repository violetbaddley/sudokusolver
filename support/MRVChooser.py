"""
MRV Chooser: Select square from a board by minimum remaining value.

Talus Baddley
October 2012
"""

import Board

def ordering(sudBoard):
    return min(sudBoard.openSquares(), key = lambda (row, col): len(sudBoard.domains[row][col]))


'''
                                    ,mmmv..__
                                /MMMMMMMMMMMMMm.
                              ,sMMMMMMMMMMMMM^MMM\
                              SM MMMMMMMMMMMM~MMMMm.
      One-line               |P^    U`````  ` \MMMM\
      MRV check?            /M ---      ^      |MMMM)
                            (M====`   / =====, |MMMMs
                            \M^``^          `` \VMMMM,
                             V <@o>   .<@@o>_   |MMM(
                             |   `)             |MP^/
                             |    __ _ )        : X )     Watch out,
                             \     . .          ` FV      we got a badass
               JD,            | AMP^`^^\Mm.      o/       over here.
           !^\ | ) .          | MP ^ `` ,V/   .  /
           |_) / ] / \        | . *^^^^`   , /  /                  (^]
      \^\  | || _|| "|        ) \        ./    |`\              .  (_\ c-\
      | ). | +| `|/ _| ___,-"` A. \.__.-`    _` X. -____       ( \ |  \|._|
       \ ^~|  V _/ _ )^  <_.   | ^-.______.v^   /|   `\.`^--._ \- \|= ||__|   .-
        \  `^     .`|    .J_    \    #MMM      //|      ^>    `^|- V   V__|  / )
       /^^Y  --._/  |   /  )    A\  /MM#MA    ,I/|     <`.      \   S- |-~. /- /
      /   |    \ -.  \ (-../    | \ MMOMMP   //  |      .Z._     |` \     `` ./
    /     \       |  `\| ^/|    |  \@MY`\ |/`/   |      ).  \    (.._`^`,`  (`
    (      |           ^  (|    |   VY`,mM.  )   |     / \*  \_./  ) `      |
   /       |             / |    |   VC CMPA /    |     /   \      `/        A
  |       .-      , .   /  |    |    VMM( )/    |     /     \      ^       / )
  |       (`\  -~`  ` ./   |    |     VMMMV     |    /       \            (_ |
  /        \ `^-._   S.    |    |     \@PA     .|    |        `^-.     -^  ) \
 (          \     `)~/     |    |      VV`     ^\   |            \\__  _..//\ \
 /           \   ~ )/       |   |      ./       |                 )````  / /  \|
(             \.  o/\           |     //       .J                 `F^^^-y /    |
|              \  /  )          |     |^`^    F                    \     U     |
-----------------------------------------------------------------------------'''
