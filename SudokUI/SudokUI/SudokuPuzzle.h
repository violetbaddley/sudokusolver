//
//  EIDocument.h
//  SudokUI
//
//  Created by Taldar Baddley on 15-10-12.
//  Copyright (c) 2012 Talus Baddley. All rights reserved.
//

#import <Cocoa/Cocoa.h>

@interface SudokuPuzzle : NSDocument {
	IBOutlet NSButton *mrvCheckbox;
	IBOutlet NSButton *lcvCheckbox;
	IBOutlet NSButton *ac3Checkbox;
	IBOutlet NSButton *solveButton;
	IBOutlet NSProgressIndicator *blinkenlichten;
	
	IBOutlet NSTextField *po;
	IBOutlet NSTextField *ps;
	IBOutlet NSTextField *boardsSurmisedField;
	IBOutlet NSTextField *backtracksField;
	IBOutlet NSTextField *fwdcheckPrunedField;
	IBOutlet NSTextField *ac3PrunedField;
	IBOutlet NSTextField *timeToSolveField;
	
	NSTask *solvingTask;
	NSLock *solvingTaskLock;
	
	NSData *infileData;
	NSMutableString *unsolvedString;
	NSString *solvedString;
	NSString *boardsSurmised;
	NSString *backtracks;
	NSString *fwdcheckPruned;
	NSString *ac3Pruned;
	NSString *timeToSolve;
}

- (IBAction)runSolve:(id)sender;
- (IBAction)terminateSolving:(id)sender;

@property (readwrite, copy) NSString *solvedString;
@property (readwrite, copy) NSString *boardsSurmised;
@property (readwrite, copy) NSString *backtracks;
@property (readwrite, copy) NSString *fwdcheckPruned;
@property (readwrite, copy) NSString *ac3Pruned;
@property (readwrite, copy) NSString *timeToSolve;

@end
