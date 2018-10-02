from noteutil.noteutil.noteutil import LineNoteUtil

nu = LineNoteUtil("test1.txt", comment="#")
# print(nu)

print(nu.nindex(lindex=0))
print(nu.nindex(content="TEST1: TEST2"))
print(nu.nindex(lindex=0, content="TEST1: TEST2"))

print(nu.nindexes(content="Data"))
print(nu.nindexes(lindexes=[6, 7, 8, 9]))
print(nu.nindexes(content="Data", lindexes=[6, 7, 8, 9]))

print(nu.lindex(content="Data2: 5%93%"))
print(nu.lindex(nindex=3))
print(nu.lindex(content="Data2: 5%93%", nindex=3))

print(nu.line(content="~~ Category 2 In category 1"))
print(nu.line(nindex=6))
print(nu.line(lindex=6))
print(nu.line(content="~~ Category 2 In category 1", nindex=6, lindex=6))

print(nu.lines(content="9"))
print(nu.lines(nindexes=[6, 7, 9]))
print(nu.lines(lindexes=[1, 2, 5]))
print(nu.lines(content="9", nindexes=[1, 2, 5], lindexes=[6, 7, 9]))

# print(nu.nindex())
# print(nu.nindex())
# print(nu.nindexes())
# print(nu.nindexes())
# print(nu.lindex())
# print(nu.lindex())
# print(nu.line())
# print(nu.line())
# print(nu.line())
# print(nu.lines())
# print(nu.lines())
# print(nu.lines())