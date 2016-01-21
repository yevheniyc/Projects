
##### Chapter 1 #######

# 1.1 - Unpacking a Sequence into Separate Variables

# Problem: 
    # Unpack N-element tuple or sequence into a collection of variables
p = (4, 5)
x, y = p # (4, 5)
data = ['ACME', 50, 91.1, (2012, 12, 21)] 
name, shares, price, (year, mon, day) = data # ('ACME', 50, 91.1, 2012, 12, 21)
# unpacking works for any iterable objects: 
    # strings, files, iterators, generators: s = 'Hello' -> a, b, c, c, e = s
# to discard certain variables use _: _, shars, price, _ = data
#============================================

# 1.2 - Unpacking elements from iterables of arbitrary length

# Problem: 
    # Unpack N elements from an iterable, but the iterable is longer than N

# unpack the first and last grades; the middle leave the way it is    
def drop_first_last(grades):
    first = grades
    return avg(middle)
grades = [3, 4, 5, 6, 4, 3, 2, 4, 5, 4]
avg_without_first_last = drop_first_last(grades) # 4

# unpack arbitrary number of phone numbers
record = ('Dave', 'dave@example.com', '773-555-1212', '847-555-1212')
name, email, *phone_numbers = record # 'Dave', 'dave@...', ['773-555-1212', '847-555-1212']

# compare average of all to the current
def compare_records_to_last(records):
    *trailing_qtrs, current_qtr = records
    trailing_avg = sum(trailing_qtrs) / len(trailing_qtrs)
    return avg_comparison(trailing_avg, current_qtr)
sales_record = [1234, 324, 5456, 324, 567, 1000] 
compare_records_to_last(sales_record) # compare the records

# the "*" syntax can be useful when iterating over a sequenc eof tuples
#+ of varying length
record = [ ('foo', 1, 2), 
           ('bar', 'hello'), 
           ('foo', 3, 4)
]

def do_foo(x, y): 
    print ('foo', x, y)

def do_bar(s): 
    print ('bar', s)
    
for tag, *args in records: # here *args represents everything after 'foo'
    if tag == 'foo': 
        do_foo(*args) # here *args unpacks the tupble into variables
    elif tag == 'bar': 
        do_bar(*args)




