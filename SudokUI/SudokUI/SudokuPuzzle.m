//
//  EIDocument.m
//  SudokUI
//
//  Created by Taldar Baddley on 15-10-12.
//  Copyright (c) 2012 Talus Baddley. All rights reserved.
//

#import "SudokuPuzzle.h"
#import "AppController.h"

@implementation SudokuPuzzle

- (id)init {
    self = [super init];
    if (self) {
		solvingTaskLock = [[NSLock alloc] init];
    }
    return self;
}








- (IBAction)runSolve:(id)sender {
	if (!unsolvedString) {
		if ([sender isKindOfClass:[NSButton class]])
			NSBeep();
		return;
	}
	
	[self terminateSolving:sender];
	[solvingTaskLock lock];
	solvingTask = [[NSTask alloc] init];
	NSTask *blockTaskR = solvingTask;
	
	NSURL *solverUrl = [[NSBundle mainBundle] URLForAuxiliaryExecutable:@"sudokusolver.py"];
	[solvingTask setLaunchPath:[solverUrl path]];
	NSMutableArray *args = [@[@"-nopo", @"-noprog", @"-stats", @"-time"] mutableCopy];
	if ([mrvCheckbox state] == NSOnState)  [args insertObject:@"-mrv" atIndex:0];
	if ([lcvCheckbox state] == NSOnState)  [args insertObject:@"-lcv" atIndex:0];
	if ([ac3Checkbox state] == NSOnState)  [args insertObject:@"-ac3" atIndex:0];
	[solvingTask setArguments:args];
	
	NSPipe *boardFeeder = [NSPipe pipe];
	NSFileHandle *boardWriter = [boardFeeder fileHandleForWriting];
	[solvingTask setStandardInput:boardFeeder];
	
	NSPipe *solutionSupplicant = [NSPipe pipe];
	NSFileHandle *solutionReader = [solutionSupplicant fileHandleForReading];
	[solvingTask setStandardOutput:solutionSupplicant];
	
	[boardWriter writeData:infileData];
	[boardWriter closeFile];
	[solvingTask launch];
	
	[solveButton setTitle:@"Stop"];
	[solveButton setKeyEquivalent:@"."];
	[solveButton setKeyEquivalentModifierMask:NSCommandKeyMask];
	[solveButton setAction:@selector(terminateSolving:)];
	[blinkenlichten startAnimation:sender];
	
	dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
		[blockTaskR waitUntilExit];
		dispatch_async(dispatch_get_main_queue(), ^{
			[blinkenlichten stopAnimation:self];
			[solveButton setTitle:@"Solve"];
			[solveButton setKeyEquivalent:@"\r"];
			[solveButton setKeyEquivalentModifierMask:0];
			[solveButton setAction:@selector(runSolve:)];
		});
		if ([blockTaskR terminationStatus] != 0)
			return;
		
		NSData *solutiveData = [solutionReader readDataToEndOfFile];
		NSString *allOutput = [[NSString alloc] initWithData:solutiveData encoding:NSUTF8StringEncoding];
		if (!allOutput)
			return;
		
		NSArray *outputLines = [allOutput componentsSeparatedByString:@"\n"];
		NSArray *solutionLines = [outputLines subarrayWithRange:NSMakeRange(1, 9)];
		[self setSolvedString:[solutionLines componentsJoinedByString:@"\n"]];
		
		NSCharacterSet *nonNumericSet = [[NSCharacterSet decimalDigitCharacterSet] invertedSet];
		[self setBoardsSurmised:[outputLines[11] stringByTrimmingCharactersInSet:nonNumericSet]];
		[self setBacktracks:[outputLines[12] stringByTrimmingCharactersInSet:nonNumericSet]];
		[self setFwdcheckPruned:[outputLines[13] stringByTrimmingCharactersInSet:nonNumericSet]];
		[self setAc3Pruned:[outputLines[14] stringByTrimmingCharactersInSet:nonNumericSet]];
		[self setTimeToSolve:[outputLines[15] stringByTrimmingCharactersInSet:nonNumericSet]];
		
		[solvingTaskLock lock];
		if (blockTaskR == solvingTask) solvingTask = nil;
		[solvingTaskLock unlock];
		
		dispatch_async(dispatch_get_main_queue(), ^{
			[self updateStuff];
		});
	});
	
	[solvingTaskLock unlock];
}

- (IBAction)terminateSolving:(id)sender {
	[blinkenlichten stopAnimation:self];
	[solveButton setTitle:@"Solve"];
	[solveButton setKeyEquivalent:@"\r"];
	[solveButton setKeyEquivalentModifierMask:0];
	[solveButton setAction:@selector(runSolve:)];

	[solvingTaskLock lock];
	
	if ([solvingTask isRunning]) {
		[solvingTask terminate];
	}
	solvingTask = nil;
	
	[solvingTaskLock unlock];
}

- (void)updateStuff {
	[ps setStringValue:solvedString];
	[boardsSurmisedField setStringValue:boardsSurmised];
	[backtracksField setStringValue:backtracks];
	[fwdcheckPrunedField setStringValue:fwdcheckPruned];
	[ac3PrunedField setStringValue:ac3Pruned];
	[timeToSolveField setStringValue:timeToSolve];
}





















- (NSString *)windowNibName {
	return @"SudokuPuzzle";
}

- (void)windowControllerDidLoadNib:(NSWindowController *)aController {
	[super windowControllerDidLoadNib:aController];
	if (!infileData) {
		[[NSApp delegate] runWelcomeWindow:self];
		dispatch_async(dispatch_get_main_queue(), ^{
			[self close];
		});
		return;
	}
	[po setStringValue:unsolvedString];
	[[NSApp delegate] puzzleDidOpen:self];
	
	[[NSNotificationCenter defaultCenter] addObserver:self
											 selector:@selector(runSolve:)
												 name:@"EISolveAllOpenPuzzlesSignal"
											   object:nil];
	[[NSNotificationCenter defaultCenter] addObserver:self
											 selector:@selector(terminateSolving:)
												 name:@"EIHaltAllSolvingsSignal"
											   object:nil];
}

- (NSData *)dataOfType:(NSString *)typeName error:(NSError **)outError {
	
	return infileData;
}

- (BOOL)readFromData:(NSData *)data ofType:(NSString *)typeName error:(NSError **)outError {
	NSMutableString *attemptedInfile = [[[[NSString alloc] initWithData:data encoding:NSUTF8StringEncoding] stringByTrimmingCharactersInSet:[NSCharacterSet whitespaceAndNewlineCharacterSet]] mutableCopy];
	if (!attemptedInfile) {
		NSError *readingError = [NSError errorWithDomain:NSCocoaErrorDomain code:NSTextReadInapplicableDocumentTypeError userInfo:[NSDictionary dictionary]];
		if (outError)  *outError = readingError;
		return NO;
	}
	
	infileData = data;
	unsolvedString = attemptedInfile;
	
	return YES;
}

- (void)dealloc {
	[[NSNotificationCenter defaultCenter] removeObserver:self];
	[self terminateSolving:nil];
	
}

- (void)canCloseDocumentWithDelegate:(id)delegate shouldCloseSelector:(SEL)shouldCloseSelector contextInfo:(void *)contextInfo {
	[self terminateSolving:nil];
	[super canCloseDocumentWithDelegate:delegate shouldCloseSelector:shouldCloseSelector contextInfo:contextInfo];
}



@synthesize ac3Pruned;
@synthesize backtracks;
@synthesize boardsSurmised;
@synthesize fwdcheckPruned;
@synthesize timeToSolve;
@synthesize solvedString;

@end
