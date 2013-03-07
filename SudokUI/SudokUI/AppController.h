//
//  AppController.h
//  SudokUI
//
//  Created by Taldar Baddley on 17-10-12.
//  Copyright (c) 2012 Talus Baddley. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface AppController : NSObject <NSApplicationDelegate> {
	IBOutlet NSWindow *welcomeWindow;
}

- (void)runWelcomeWindow:(id)sender;
- (void)puzzleDidOpen:(id)sender;

- (IBAction)solveAllOpenPuzzles:(id)sender;
- (IBAction)haltAllSolvings:(id)sender;

@end
