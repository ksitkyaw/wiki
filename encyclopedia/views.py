from django.shortcuts import render

from . import util
import random
import markdown2

#markdown2 handles the conversion of markdown to html
def index(request):
#When a post request was made, the inpt to search  store in data and list the entries using a util function
    if request.method == "POST":
        data = request.POST['q']
        entries = util.list_entries()
#To check if the search input(data) match any of the entries, for loop is used.
        for entry in entries:
            #if data matches any of the existing  entries, the entry.html is rendered
            if data.lower() == entry.lower(): #lower function used for case insensitivity
                content = util.get_entry(entry)
                htmlcontent=markdown2.markdown(content) #this convert markdown to html tags
                return render(request, "encyclopedia/entry.html", {
                    "content": htmlcontent,
                    "title": entry
                })
            #this case is take place if data is a substring of any existing entry
            elif data.lower() in entry.lower():
                searchresults= []
                #I loop again to find all matching entries.Since there is a return value at the end, the above for loop will  
                #break after finding a match entry so there'll always be one searchresult
                for entry in entries:
                    if data.lower() in entry.lower():
                        searchresults.append(entry)

                return render(request, "encyclopedia/searchresults.html", {"title" : data, "searchresults": searchresults})
        #this is the third case that you don't find any entry that match so the error page is rendered.
        return render(request, "encyclopedia/error.html", {"title": data})
    #this is for get request
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, TITLE):
#this function is to redirect you to corresponding entry page when you click a link of an entry

    content = util.get_entry(TITLE)
    htmlcontent=markdown2.markdown(content)

    if not content:
        return render(request, "encyclopedia/error.html" , {"title": TITLE})
    return render(request, "encyclopedia/entry.html", {
        "content": htmlcontent,
        "title": TITLE
    })

def create(request):
    #to create an entry, a post request is made with title and content as inputs
    if request.method == "POST":
        title=request.POST['title']
        content=request.POST['content']
        entries=util.list_entries()
        #loop through the enties to find if there is an existing entry with the same name
        for entry in entries:
            if title == entry: #if there is, Error page is rendered.
                
                return render(request, "encyclopedia/createError.html", {
                    "title": entry
                })
        #if not, the new page is created and saved in entries directory too
        util.save_entry(title, content)
        return render(request, "encyclopedia/entry.html", {
            "content": markdown2.markdown(content),
            "title": title
        })
    #this is for get requests
    return render(request, "encyclopedia/create.html")

def edit(request, title): 
    content=util.get_entry(title)

    if request.method == "POST":
        newcontent = request.POST['content']
        util.save_entry(title, newcontent)
        #It just save the new content from the post request.the title can't be changed
        return render(request, "encyclopedia/entry.html", {
            "content": markdown2.markdown(newcontent),
            "title": title
        })
    
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })

def randompage(request):
    entries=util.list_entries()
    rand = random.randint(0, len(entries)-1) #pick a random integer
    entrytitle = entries[rand] #using the random integer as index, a random entry is picked
    content = util.get_entry(entrytitle)
    htmlcontent=markdown2.markdown(content)
    #render entry.html with content from above random entry
    return render(request, "encyclopedia/entry.html", {
        "title": entrytitle,
        "content": htmlcontent
    })