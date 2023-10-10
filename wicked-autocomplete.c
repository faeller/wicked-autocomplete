#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <unistd.h>

void sigIntHandler(int signal)
{
    printf("\nAborting...\n");
    exit(1);
}

// Concatenates a vector of strings.
char* concat(int strc, const char** strv)
{
    // Find size of all arg.
    int bufSize = 0;
    for (int i = 1; i < strc; i++)
    {
        // String size + 1 char for ' '.
        bufSize += strlen(strv[i]) + 1;
    }
    char* buf = (char*)malloc(bufSize + 1);
    char* cursor = buf;
    for (int i = 1; i < strc; i++)
    {
        // Copy the arg into the buffer and advance the cursor by its length.
        const int strSize = strlen(strv[i]);
        memcpy(cursor, strv[i], strSize);
        cursor += strSize;
        // If not the last argument, append a space, otherwise a null terminator.
        if (i < strc - 1)
            *cursor = ' ';
        else 
            *cursor = '\0';
        cursor++;
    }
    return buf;
}

size_t getLineCount(char* text)
{
    size_t len = strlen(text);
    size_t lineCount = 0;
    for (int i = 0; i < len; i++)
    {
        if (text[i] == '\n')
            lineCount++;
    }
    return lineCount;
}

// Get a specific line from a text. Returns null if out of bounds.
char* getLine(char* text, int line)
{
    if (line >= getLineCount(text) || line < 0) return (char*)2;

    char* result = text;
    int curLine = 0;
    int len = 0;
    while (result)
    {
        // Get strlen.
        len = 0;
        while (result[len] != '\n')
            len++;
        if (curLine == line)
        {
            result[len] = '\0';
            break;
        }
        result += len + 1;
        curLine++;
    }
    char* str = calloc(sizeof(char), strlen(result) + 1);
    strcpy(str, result);
    result[len] = '\n';
    return str;
}

#define BUF_SIZE 4096

char* getSuggestions(const char* mask, const char* input)
{
    char* buf = (char*)calloc(sizeof(char), BUF_SIZE);
    if (!buf) return 0;

    // Open a pipe to stderr.
    int outPipe[2]; 
    if (pipe(outPipe)) return 0;
    int stdErrOld = dup(STDERR_FILENO); // Save the stderr connection for later.
    dup2(outPipe[1], STDERR_FILENO); // Redirect stderr to the pipe.

    // Run the command and get the output.
    system(input);
    read(outPipe[0], buf, BUF_SIZE);

    // Reconnect stderr.
    dup2(stdErrOld, STDERR_FILENO);

    // Find the command table.
    char* cursor = buf;
    int maskLen = strlen(mask);
    while (*cursor)
    {
        if (strncmp(cursor, mask, maskLen) == 0)
            break;
        cursor++;
    }
    cursor += maskLen;

    return cursor;
}

int main(const int argc, const char** argv)
{
    // Hook signals.
    signal(SIGINT, sigIntHandler);

    // Concatenate user args to one string.
    char* userInput = concat(argc, argv);

    // Get commands.
    char* b = getSuggestions("ptions:\n", userInput);
    if (!b) return 1;

    // Print each command.
    int lineCount = getLineCount(b) - 1;
    for (int i = 0; i < lineCount; i++)
    {
        char* line = getLine(b, i);
        if (line && line[0] == ' ' && line[1] == ' ' && line[2] != ' ')
        {
            // Split off the first word.
            line += 2;
            size_t len = strlen(line);
            for (int k = 0; k < len; k++)
            {
                if (line[k] == ' ')
                {
                    line[k] = '\0';
                    break;
                }
            }
            printf("%s\n", line);
        }
    }

    // Clean up.
    free(userInput);
    return 0;
} 
