from django.shortcuts import render, HttpResponse 
from django.http import JsonResponse
from forest.models import Post, Label
from django.contrib import messages
from json import loads , dumps
import requests 
from random import choice
# global verables 
# making color list to send it for template to use random color functianality 
color_list = ["danger" , "warning" ,"primary" ,"secondary" , "success" , "info" ,"light" , "dark"  ]

# specific functions 
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# main functions 
def forest_movies(request):
    # specific verables
    label_selected = False
    # making all section inactive as default
    active_hollywood = None
    active_bollywood = None
    active_anima = None
    active_animation = None
    # back home button for scrapper
    back_home_button = False
    # declaring next or previous as default
    disable_next = False
    disable_previous = False
    # for showing banner
    show_banner = True
    # for default page
    at_page_no = 1
    # declaring a content for first page
    content_start = 0
    content_end = 9
    # checking the request
        # if request is post don't show back_home_button
        back_home_button = False
        # checking for which section user send a request
        # if user request for hollywood page
        if request.POST.get("hollywood"):
            # changing all movies_post with hollywood related posts
            all_movies_post = Post.objects.filter(section="hollywood").order_by("sno").reverse()
            # getting how many pages will built with hollywood content avalable in database
            len_pages = len(all_movies_post)/9
            # parsing a page_id to know "next previous" button's that user is at which page
            page_id = "hollywood"
            # changing page no to firest as default because session will save the previous page no
            at_page_no = 1

        # if user request for bollywood page
        elif request.POST.get("bollywood"):
            # changing all movies_post with bollywood related posts
            all_movies_post = Post.objects.filter(section="bollywood").order_by("sno").reverse()
            # getting how many pages will built with bollywood content avalable in database
            len_pages = len(all_movies_post)/9
            # parsing a page_id to know "next previous" button's that user is at which page
            page_id = "bollywood"
            # set page id in session
            # request.session["page_id"] = page_id
            # changing page no to firest as default because session will save the previous page no
            at_page_no = 1

        # if user request for anima page
        elif request.POST.get("anima"):
            # changing all movies_post with anima related posts
            all_movies_post = Post.objects.filter(section="anima").order_by("sno").reverse()
            # getting how many pages will built with anima content avalable in database
            len_pages = len(all_movies_post)/9
            # parsing a page_id to know "next previous" button's that user is at which page
            page_id = "anima"
            # changing page no to firest as default because session will save the previous page no
            at_page_no = 1

        # if user request for hollywood page
        elif request.POST.get("animation"):
            # changing all movies_post with animation related posts
            all_movies_post = Post.objects.filter(section="animation").order_by("sno").reverse()
            # getting how many pages will built with animation content avalable in database
            len_pages = len(all_movies_post)/9
            # parsing a page_id to know "next previous" button's that user is at which page
            page_id = "animation"
            # changing page no to firest as default because session will save the previous page no
            at_page_no = 1
        # if user request for any category
        if request.POST.get("label"):
            # getting lable name
            selected_label = request.POST["label"]
            # getting a page id where user is now if user is in download page so getting section from request perameter
            
            if request.POST.get("section_of_download_page"):
                page_id = request.POST["section_of_download_page"]
            else:
                page_id = request.session["page_id"]
                
            # updating content with related category and section
            all_movies_post = Post.objects.filter(
                category__icontains=selected_label, section=page_id).order_by("sno").reverse()
            # making page lenght one because i want to show label content in single page
            len_pages = 1
            # making a label_selected True because i want to show all content in singel page
            label_selected = True

        # if user send a request for next page
        if request.POST.get("next"):
            # getting the page no where user is now
            at_page_no = int(request.POST["next"])
            # updating page no if someone request for next page
            at_page_no += 1
            # getting a page id where user is now
            page_id = request.POST["page_id"]
            # updating content with related page_id content
            all_movies_post = Post.objects.filter(section=page_id).order_by("sno").reverse()
            # getting lenth of content
            len_pages = len(all_movies_post)/9

        # if user send a request for previous page
        if request.POST.get("previous"):
            # getting the page no where user is now
            at_page_no = int(request.POST["previous"])
            # updating page no if someone request for previous page
            at_page_no -= 1
            # getting a page id where user is now
            page_id = request.POST["page_id"]
            # updating content with related page_id content
            all_movies_post = Post.objects.filter(section=page_id).order_by("sno").reverse()
            # getting lenth of content
            len_pages = len(all_movies_post)/9
    # if request is not post it means user refreshes or either try to scrape
    else:
        # getting previous page if exists in sesssion
        get_session_page_id = request.session.get("page_id")
        # getting previous page number if exists
        session_page_no = request.session.get("at_page_no")
        # checking session page exists or not
        if get_session_page_id != None and get_session_page_id != "mother_fucker":
            # making content related to previous page_id
            all_movies_post = Post.objects.filter(section=get_session_page_id).order_by("sno").reverse()
            # getting lenght
            len_pages = len(all_movies_post)/9
            # changing page id to previous page id
            page_id = get_session_page_id

        # checking session page_no exists or not
        if session_page_no != None:
            # changing page no with session page no
            at_page_no = session_page_no
        # if session not means session is empty
        if get_session_page_id == None or get_session_page_id == "mother_fucker":
            # making content related to motherfucker posts
            all_movies_post = Post.objects.filter(section="mother_fucker").order_by("sno").reverse()
            # getting length
            len_pages = len(all_movies_post)/9
            # setting default page id and banner as motherfucker
            page_id = "mother_fucker"
            # showing back_home button instead of previous or next button's
            back_home_button = True

    # getting all labels avalable in database
    labels = Label.objects.all()
    # making empty year list 
    year = []
    # making main for main categorey 
    main = []
    # making other labels list 
    other = []
    # for loop to filter the labels 
    for lab in labels.iterator():
        # if categorery is in numbers so put it into year section 
        if lab.categories.isdigit():
            year.append(lab.categories)
        # if category is language or main so put it into main 
        elif lab.categories.lower() == "movie" or lab.categories.lower() == "tvseries" or lab.categories.lower() == "english" or lab.categories.lower() == "hindi" or lab.categories.lower() == "spanish" or lab.categories.lower() == "japanese":
            main.append(lab.categories)
        # and put other categorey into others 
        else:
            other.append(lab.categories)
    # if someone refresh applying changes according to the page_id
    if page_id == "hollywood":
        active_hollywood = " bg-success"
    elif page_id == "bollywood":
        active_bollywood = " bg-success"
    elif page_id == "anima":
        active_anima = " bg-success"
    elif page_id == "animation":
        active_animation = " bg-success"
    else:
        pass

    # checking back button is avalable or not if yes So giving an error
    if back_home_button:
        messages.error(
            request, "You'r session has been expired! Go back to the home")

    # set page id in session according to the request
    request.session["page_id"] = page_id
    # set page in session according to the next or previous request
    request.session["at_page_no"] = at_page_no
    # to clearing the expired sessions from database
    request.session.clear_expired()

    # deciding how much content will display in every changed page
    # checking if label is not selected show 9 content in every page
    if not label_selected:
        content_end = at_page_no * 9
        content_start = content_end - 9
    # but if label is selected show content 0 from infinite
    else:
        content_start = 0
        content_end = ""
     # checking the next page is avalable or not if not disable next button
    if len_pages <= at_page_no:
        disable_next = True
    # check of page no is one if yes so disable previous button
    if at_page_no == 1:
        disable_previous = True
    # checking the visited page is first or not if not do disable the banner
    if at_page_no > 1:
        show_banner = False
    # if "float len_page" is bigger then "int len_page" so changing it's value into plus one
    if int(len_pages) < len_pages:
        len_pages += 1
    # making a context to send data to template
    context = {'all_movies_post': all_movies_post, "content_end": str(content_end),
               "content_start": str(content_start), "show_banner": show_banner, "at_page_no": at_page_no, "disable_next": disable_next,
               "disable_previous": disable_previous, "banner": page_id, "page_id": page_id, "back_home_button": back_home_button,
               "len_pages": int(len_pages), "active_hollywood": active_hollywood, "active_bollywood": active_bollywood, "active_anima": active_anima,
               "active_animation": active_animation, "year": year ,"main":main ,  "other":other , "color_list":color_list }
    # returning a responce
    return render(request, 'forest/movies.html', context)
# personal function for devlopers to create the posts


def make_post(request):
    # making default verables for json response
    # creating a boolean for to know error was genetated or not
    error_generated = False
    # defalting post_success to False
    post_success = False
    # making new_label_added False
    new_label_added = False
    # making a error content none
    error = None
    # making a post_id None as default
    post_id = None
    # making a list for pre_defined_sections
    all_sections_list = ["hollywood", "bollywood", "anima", "animation"]
    # making data as default 
    section  = None
    logo_link = None 
    screen_shots = None
    title = None
    title_caption = None
    discreption = None
    download_links = None
    other_download_links = None
    trailer_link = None
    keywords = None
    # gettting prerequizits for creating a post
    # getting section
    # trying to getting all perameters
    try: 
        section = request.GET["section"]
        # getting label
        label = request.GET["label"]
        # getting logo_link
        logo_link = request.GET["logo_link"]
        # getting screenshots links
        screen_shots = request.GET["screen_shots"]
        # getting title
        title = request.GET["title"]
        # getting title_caption
        title_caption = request.GET["title_caption"]
        # getting content
        discreption = request.GET["discreption"]
        # getting download links
        download_links = request.GET["download_links"]
        # getting other downlaod links 
        other_download_links = request.GET["other_download_links"]
        # getting traiter_link
        trailer_link = request.GET["trailer_link"]
        # getting keywords for post 
        keywords = request.GET["keywords"]
    except Exception as e:
        error_generated = True
        error = f"You need to put all perameter to success this post ! Ression {e}"
    # if error not occure  while taking perameters so moving forward 
    if not error_generated:
        # checking if given data is in right format or not
        # checking the sections is in correct format
        if section not in all_sections_list or section.isspace():
            error_generated = True
            error = "Bro you'r section is wrong section can be only bollywood , bollywood , anima , animation"
        # checking label list is empty or not
        elif len(label) == 0 or label.isspace():
            error_generated = True
            error = "You need to specify at least one label"
        # checking  logo link
        elif len(logo_link) == 0 or logo_link.isspace():
            error_generated = True
            error = "You'r logolink is empty!"
        # getting screenshot links
        elif len(screen_shots) == 0 or screen_shots.isspace():
            error_generated = True
            error = "You need to give at least one screenshot link"
        # checking title is empty or not
        elif len(title) == 0 or title.isspace():
            error_generated = True
            error = "You title must be something"
        # checking title should not be less then 1 world
        elif len(title_caption) == 0 or title_caption.isspace():
            error_generated = True
            error = "You need to give at least one world of title_caption"
        # checking discreption is empty or not
        elif len(discreption) == 0 or discreption.isspace():
            error_generated = True
            error = "You discreption is nothing please put some content here"
        elif len(trailer_link) == 0 or trailer_link.isspace():
            error_generated = True
            error = "You need to put trailer link of movie from YouTube"
        elif len(download_links) == 0 or download_links.isspace():
            error_generated = True
            error  = "You can make download empty"
        elif len(keywords) == 0 or keywords.isspace():
            error_generated = True
            error = "You need to put at least one keyworld for making a post"
        
        elif Post.objects.filter(title=title).exists():
            error_generated = True
            error = "You can't duplicate the post. This post exists already"
        else:
            # checking new label string has wide spaces or not if yes removing all spaces
            label = "".join(label.split())
            # spliting string with comas
            list_of_given_labels = label.split(",")
            # iterating loop for each object in label list
            for i in range(len(list_of_given_labels)):
                # checking if Label data contains lable already in database
                if Label.objects.filter(categories__icontains=list_of_given_labels[i]):
                    pass
                # if lable is not in database so add it
                else:
                    New_label = Label(categories=list_of_given_labels[i])
                    New_label.save()
                    new_label_added = True
            # if each credentials are right so creating a post
            Create_new_post = Post(section=section, category=label, logo_link=logo_link,
                                    screen_shots=screen_shots, title=title, title_caption=title_caption,
                                    content=discreption, download_links=download_links,other_download_links= other_download_links,
                                    trailer_link=trailer_link,
                                    keywords = keywords,
                                    )
            Create_new_post.save()
            post_success = True
        # if post not succed it means post already exists
        if post_success:
            # if post succed it means new post was created and need to show post_id
            new_post = Post.objects.get(title=title)
            post_id = str(new_post.sno)
        else:
            pass
        # if error generated while getting perameters do don't do anything just pass it away 
    else:
        pass
    responseData = {
        "error": error,
        "error_generated": error_generated,
        "post_success": post_success,
        "new_label_added": new_label_added,
        "section": section,
        "logo_link": logo_link,
        "list_of_labels": label,
        "list_of_screen_shots": screen_shots,
        "title": title,
        "title_caption": title_caption,
        "discreption": discreption,
        "download_links": download_links,
        "other_download_links":other_download_links,
        "trailer_link": trailer_link,
        "post_id": post_id,
        "keywords":keywords,
    }
    return JsonResponse(responseData)
# this is for delete content from database 
def delete_post(request):
    # getting post id to delete
    reasion = "You give existing post_id" 
    post_deleted = True
    try:
        access_key = request.GET["assess_key"]
        post_id = int(request.GET["post_id"])
        deleting_post = Post.objects.get(sno=post_id)
        deleting_post.delete()
    except Exception as e:
        reasion = str(e)
        post_deleted = False
    responseData = {"Delete_status":post_deleted , "Reasion":reasion}
    return JsonResponse(responseData)
    
# this is for update content in database 
def update_posts(request):
    # making as default
    update_success = False
    add_success = False
    post_id = None
    if request.GET.get("post_id"):
        # getting post_id from request 
        post_id = str(request.GET["post_id"])
        # getting real post assesoiated with post_id Note :  the realpost is not a queryset object it is an single object in which we can direclty use .save() function
        try:
            real_post = Post.objects.get(sno=post_id)
        except:
            early_response = {"Success":False,
                            "Ression":"Post_id does not exists"
            }
            return JsonResponse(early_response)
        # if sender give update perameter 
        if request.GET.get("update"):
            # getting new content from the value of update perameter 
            new_content = loads(request.GET["update"])
            for column , content in new_content.items():
                if column.lower() == "section":
                    real_post.section = content
                    update_success = True
                elif column.lower() == "label" or column.lower() == "category":
                    real_post.category = content
                    update_success = True
                elif column.lower() == "logo_link":
                    real_post.logo_link = content
                    update_success = True
                elif column.lower() == "screen_shots":
                    real_post.screen_shots = content
                    update_success = True
                elif column.lower() == "title":
                    real_post.title = content
                    update_success = True
                elif column.lower() == "title_caption":
                    real_post.title_caption = content
                    update_success = True
                elif column.lower() == "content":
                    real_post.content = content
                    update_success = True
                elif column.lower() == "trailer_link":
                    real_post.trailer_link = content
                    update_success = True
                else:
                    continue
            real_post.save()

        if request.GET.get("add"):
            # getting value of add peramater 
            new_content = loads(request.GET["add"])
            for column , content in new_content.items():
                if column.lower() == "label" or column.lower() == "category":
                    real_post.category += content
                    add_success = True
                elif column.lower() == "screen_shots":
                    real_post.screen_shots += content
                    add_success = True
                elif column.lower() == "title":
                    real_post.title += content
                    add_success = True
                elif column.lower() == "title_caption":
                    real_post.title_caption += content
                    add_success = True
                elif column.lower() == "content":
                    real_post.content += content
                    add_success = True
                else:
                    continue
            real_post.save()

        # if request for adding downlaod links 
        if request.GET.get("add_download_links"):
            # getting new links
            new_links = request.GET["add_download_links"]
            # making  a download links string into python dict
            new_download_links = loads(new_links)
            # previous download links Note: the links that are stored in database
            old_download_links = loads(real_post.download_links)
            # mergin both dicts with eachother Note i am using new pipe(|) feature of python 3.9. feature which is not in previous versions
            updated_download_links = old_download_links | new_download_links
            # changing download links in database | Note: (important) i use dumps function here to store it in string format 
            real_post.download_links = dumps(updated_download_links)
            real_post.save()
            add_success = True
        if request.GET.get("add_other_download_links"):
             # getting new links
            new_links = request.GET["add_other_download_links"]
            # making  a download links string into python dict
            new_download_links = loads(new_links)
            # previous download links Note: the links that are stored in database
            old_download_links = loads(real_post.other_download_links)
            # mergin both dicts with eachother Note i am using new pipe(|) feature of python 3.9. feature which is not in previous versions
            updated_download_links = old_download_links | new_download_links
            # changing download links in database | Note: (important) i use dumps function here to store it in string format 
            real_post.download_links = dumps(updated_download_links)
            real_post.save()
            add_success = True
        else:
            pass
    else:
        pass
    context = {"Update_success":update_success,
                "Add_success":add_success,
                "Post_id":post_id,
    }
    return JsonResponse(context)


# this is for download page
def download(request):
    # getting post_serial_no
    post_id = request.GET["post_id"]
    # fetching post content with this serial_no from database
    post = Post.objects.get(sno=post_id)
    # getting download_links make them in json format
    download_links_list = loads(post.download_links)
    # getting other download links and make then into json format 
    other_links_list  = loads(post.other_download_links)
    # making a empty stream link list default because i have to change download links to stream link
    stream_links_list = {}

    # download link what i have 
    # type 1:
    # https://drive.google.com/uc?id=id_of_post&export=download
    # type 2:
    # https://drive.google.com/file/d/id_of_post/view 


    # stream link with i want to make 
    # https://drive.google.com/file/d/id_of_post/preview
    # converting  downlaod links to stream links
    for quality, links in download_links_list.items():
        # handling both type of download links to make proper stream link 
        if "uc?id=" in links:
            # getting if from download link Note: I use partition method here because if something went wrong the string will be empty
            id_of_download_link = links.partition("/uc?id=")[2].partition("&export=download")[0]
        if "/file/d/" in links:
            # getting id from download link 
            id_of_download_link = links.partition("/file/d/")[2].partition("/view")[0]
        # making a string of google drive streaming link
        ready_stream_url = f"https://drive.google.com/file/d/{id_of_download_link}/preview"
        stream_links_list[quality] = ready_stream_url

    # making a list of screenshots by spliting with space
    screen_shots_list = post.screen_shots.split(" ")
    # incrementing views count if request from new ip adress
    # getting the list of ips that are resently viewed in post 
    list_of_ips = post.ips.split(",")
    # getting current user ip 
    current_user_ip = get_client_ip(request= request) 
    # if lenght of resent ips is more than 100 so removing all ips 
    if len(list_of_ips) > 100:
        post.ips = "127.0.0.1,"
        post.save()
    # if new ip found so incrementing the ip in ips list 
    if str(current_user_ip) not in list_of_ips:
        post.ips += f"{current_user_ip},"
        post.views_count +=1
        post.save()
    else:
        pass
    # making list of labels 
    labs_list = post.category.split(",")
    # ---------------------this is the code related to the wepush notifications -----------------
    # deciding a goup name for my subscribers 
    group_name = "my_subscriber"
    # making a dict of group(perameter name ) to send it to context 
    webpush = {"group": group_name}
    # making a final context to send it to tamplete 
    context = {"post": post, "download_links_list": download_links_list,"other_links_list": other_links_list,
               "stream_links_list": stream_links_list,
               "screen_shots_list": screen_shots_list , "color_list":color_list,
               "labs_list":labs_list,
               "webpush":webpush,
               }
    return render(request, "forest/download.html", context)


def stream(request):
    # getting stream link
    link = request.GET["link"]
    context = {"link": link}
    return render(request, "forest/stream.html", context)




