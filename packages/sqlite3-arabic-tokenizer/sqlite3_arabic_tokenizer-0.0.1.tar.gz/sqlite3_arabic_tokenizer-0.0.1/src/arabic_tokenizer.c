// Copyright (c) 2024 Shahriar Nasim Nafi, MIT License
// https://github.com/GreentechApps/sqlite3_arabic_tokenizer.py


#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "sqlite3ext.h"

// lib header
#include "arabic_tokenizer.h"

// tokenizer
#include "sqlite3-arabic-tokenizer.h"


#ifdef _WIN32
__declspec(dllexport)
#endif
    int sqlite3_arabic_tokenizer_init(sqlite3* db, char** errmsg_ptr, const sqlite3_api_routines* api) {
  
    const char* enable = getenv("ARABIC_TOKENIZER_ENABLE");
    if (enable != NULL && strcmp(enable, "0") == 0) {
        return SQLITE_OK;
    }
    if (enable != NULL) {
        sqlite3_sqlitearabictokenizer_init(db, errmsg_ptr, api);
        return SQLITE_OK;
    }

    return SQLITE_OK;
}
