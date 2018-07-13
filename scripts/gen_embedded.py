#!/usr/bin/env python

import os, os.path, sys


MAX_SLICE = 70

def as_byte(data):
    if sys.version_info < (3,):
        return ord(data)
    else:
        return data


print("""
#include "internal/Embedded.h"

#include <string>
#include <unordered_map>

namespace {
""")

files = []
index = 1

for f in sys.argv[1:]:
    bytes = open(f, 'rb').read()
    name = "fileData%d" % index
    index += 1
    files.append((name, os.path.basename(f), len(bytes)))
    print('const char %s[] = {' % name)
    for start in range(0, len(bytes), MAX_SLICE):
        print('' + "".join(["'\\x%02x'," % as_byte(x) for x in bytes[start:start+MAX_SLICE]]))
    print('0 };')

print("""
std::unordered_map<std::string, EmbeddedContent> embedded = {
""")

for name, base, length in files:
    print('{"/%s", { %s, %d }},' % (base, name, length))

print("""
};

}  // namespace

const EmbeddedContent* findEmbeddedContent(const std::string& name) {
    const auto found = embedded.find(name);
    if (found == embedded.end()) {
        return nullptr;
    }
    return &found->second;
}
""")

