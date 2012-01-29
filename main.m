#import <stdio.h>
#import <Cocoa/Cocoa.h>
#import <FScript/FScript.h>

int main(int argc, char * argv[])
{
    FSInterpreter * interpreter = [[FSInterpreter alloc] init];
    NSString * script = [NSString stringWithContentsOfFile: @"MicroChips.st"];
    FSInterpreterResult * result = [interpreter execute: script];
    if ([result isOk]) {
        id r = [result result];
        if (r == nil) {
            puts("nil");
        } else {
            puts([[r printString] UTF8String]);
        } 
    } else {
        puts([[NSString stringWithFormat:@"%@ , character %d\n", [result errorMessage], [result errorRange].location] UTF8String]);
    }
    return 0;
}
