YUNGTWEETZY
============
nltk.download()
All Packages
Download packages:
cmudict
punkt

<!-- Part 3:  Project Writeup / Reflection

Please prepare a short document with the following sections (one per project, not per person):
Project Overview: What were you trying to accomplish?  What was your general approach?
Implementation: How does your code work?  What libraries did you use?  How would someone (for instance a NINJA) run your code?  What data structures (e.g. lists, dictionaries) did you use in your program and why?
Results: If you did some text analysis, what interesting things did you find?  If you created a program that does something interesting (e.g. a Markov text synthesizer), provide a few interesting examples of the program's output.
Reflection: from a process point of view, what went well? what could you improve?  For instance, were there specific strategies for better coordinating on a software project with a partner?  Was your project appropriately scoped?  Did you have a good plan for unit testing?
Turning in Your Work:

Code: push your completed code to the "master" Git repository (depending on which partner's repository is being used to work on the project).
Writeup: push your completed writeup as a pdf file called writeup_and_reflection.pdf.
Your code and your writeup should be contained entirely within a sub-directory called hw5 (following the pattern of past assignments). -->

REFLECTION
============

Overview:
For project YUNGTWEETZY, Dennis Chen and I wanted to convert Twitter streams into a rap composition for any generic popular song instrumentals. Our general approach was step-wise. First, we wanted...

Implementation:
Our program works in a step-wise factory-like way. It starts with pulling partially-processed twitter feeds that are tailored to specific search terms.

Results:
Here's an excerpt of our rap composition.

Reflection:
What went well?
Finding the resources to build our program turned to be much easier than we expected.

What could we improve?
To better organize our rhymes, we could progress by seeing which tweets were most relevant to each other. With time, things we could have tried are sentiment analysis and Markov mapping. 

What are some opportunities for better strategies?

Did we have a good plan for unit testing?
During the first part of our program where we categorize our twitter rhymes, we implemented quite a bit of unit testing functions to collect as many sensical rhymes as possible. The debugging experience during the actual ryhme scheme generation is completed based on print debugging.