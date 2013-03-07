//
//  AppController.m
//  SudokUI
//
//  Created by Taldar Baddley on 17-10-12.
//  Copyright (c) 2012 Talus Baddley. All rights reserved.
//

#import "AppController.h"

@implementation AppController

- (void)runWelcomeWindow:(id)sender {
	[welcomeWindow makeKeyAndOrderFront:sender];
}

- (void)puzzleDidOpen:(id)sender {
	[welcomeWindow orderOut:sender];
}

- (IBAction)solveAllOpenPuzzles:(id)sender {
	[[NSNotificationCenter defaultCenter] postNotificationName:@"EISolveAllOpenPuzzlesSignal" object:self];
}

- (IBAction)haltAllSolvings:(id)sender {
	[[NSNotificationCenter defaultCenter] postNotificationName:@"EIHaltAllSolvingsSignal" object:self];
}

@end
