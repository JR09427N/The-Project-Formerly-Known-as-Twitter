from flask import Flask, request, redirect, render_template, session, make_response

import json
import boto3
import uuid
from boto3.dynamodb.conditions import Key
from datetime import datetime
from zoneinfo import ZoneInfo


AWSKEY = 'AKIAXEVXYLTKKVQZ6CZ3'
AWSSECRET = '--[Romoved From File]--'
PUBLIC_BUCKET = 'jr09427n-web-public'
STORAGE_URL = 'https://s3.amazonaws.com/' + PUBLIC_BUCKET + '/'
commentId = ''

def get_table(name):
    dbclient = boto3.resource(service_name='dynamodb',
                        region_name='us-east-1',
                        aws_access_key_id=AWSKEY,
                        aws_secret_access_key=AWSSECRET
                        )

    table = dbclient.Table(name)
    return table


def get_public_bucket():
    s3client = boto3.resource(service_name='s3',
                          region_name='us-east-1',
                          aws_access_key_id=AWSKEY,
                          aws_secret_access_key=AWSSECRET
                          )
    bucket = s3client.Bucket(PUBLIC_BUCKET)
    return bucket


#**************************************************************** Final Project Start ******************************************************************************************

def login():
    email = request.args.get('email', '')
    password = request.args.get('password', '')

    if email == '' or password == '':
        return {'result':'Bad Login'}

    table = get_table('Users')
    item = table.get_item(Key={'email':email})
    if 'Item' not in item:
        return {'result':'Email not found'}

    user = item['Item']
    if password != user['password']:
        return {'result':'Password not valid.'}

    # at this point, the email and password are correct
    session['email'] = user['email']
    session['username'] = user['username']

    result = {'result':'OK'}
    response = make_response(result)

    return response

def signup():

    def contains_char(email, char):
        if char in email:
            return True
        return False

    table = get_table('Users')

    email = request.args.get('email', '')
    username = request.args.get('username', '')
    password = request.args.get('password', '')

    email_item = table.get_item(Key={'email':email})
    if 'Item' in email_item:
        return {'result':'Email already taken'}

    if not contains_char(email, '@') or not contains_char(email, '.'):
        return {'result':'Email not valid.'}

    if email == '' or username == '' or password == '':
        return {'result':'Bad Signup'}

    session['email'] = email
    session['username'] = username

    newUser = {
        'email':email,
        'username':username,
        'password':password,
        'profilepic':'generic.png'
        }

    table.put_item(Item=newUser)

    result = {'result':'OK'}
    response = make_response(result)

    return response

def final_getpfp():
    table = get_table('Users')

    username = request.args.get('username')

    for item in table.scan()['Items']:
        if username == item['username']:
            return{'result':item['profilepic']}


def final_getemail():
    table = get_table('Users')

    username = request.args.get('username')

    for item in table.scan()['Items']:
        if username == item['username']:
            return{'result':item['email']}

def final_uploadpfp():
    bucket = get_public_bucket()
    table = get_table('Users')

    email = request.form.get('email')
    file = request.files["file"]
    filename = file.filename

    uid =  str(uuid.uuid4()) + '/jpeg'
    if filename.endswith('.png'):
        uid = str(uuid.uuid4()) + '/png'

    bucket.upload_fileobj(file, filename, ExtraArgs={'ContentType': uid})

    table.update_item(
        Key={'email': email},
        UpdateExpression='set profilepic=:r',
        ExpressionAttributeValues={':r':filename}
        )

    return {'results': 'OK'}

def final_uploadpost():
    table = get_table('Posts')

    postID = str(uuid.uuid4())
    username = request.form.get('username')
    content = request.form.get('content')
    today = datetime.now(ZoneInfo('America/New_York')).strftime("%I:%M %p")
    childID = str(uuid.uuid4())

    upload = {'PostID': postID, 'Username': username, 'Content': content, 'Date': today, 'ChildID': childID}

    table.put_item(Item=upload)

    return {'results':'OK'}


def final_getposts():
    table = get_table('Posts')
    result = []

    username = request.args.get('username')

    for item in table.scan()['Items']:
        if username == item['Username']:
            s = {'PostID':item['PostID'], 'Username':item['Username'], 'Content':item['Content'], 'Date':item['Date'], 'ChildID':item['ChildID']}
            result.append(s)

    sorted_result = sorted(result, key=lambda x: datetime.strptime(x['Date'], '%I:%M %p'), reverse=True)

    return{'result':sorted_result}

def final_listfeedposts():
    table = get_table('Posts')
    result = []
    for item in table.scan()['Items']:
        s = {'PostID':item['PostID'], 'Username':item['Username'], 'Content':item['Content'], 'Date':item['Date'], 'ChildId':item['ChildID']}
        result.append(s)

    sorted_result = sorted(result, key=lambda x: datetime.strptime(x['Date'], '%I:%M %p'), reverse=True)

    return{'result':sorted_result}

def final_listonepost():
    table = get_table('Posts')
    result = []

    postId = request.args.get('postId')
    global commentId

    for item in table.scan()['Items']:
        if postId == item['PostID']:
            s = {'PostID':item['PostID'], 'Username':item['Username'], 'Content':item['Content'], 'Date':item['Date'], 'ChildID':item['ChildID']}
            commentId = item['ChildID']
            result.append(s)

    comm_result = []
    table = get_table('Comments')
    for item in table.scan()['Items']:
        if commentId == item['CommentID']:
            s = {'ParentID':item['ParentID'], 'Text':item['Text'], 'Date':item['Date'], 'CommentID':item['CommentID'], 'Username': item['Username']}
            comm_result.append(s)

    sorted_comm_result = sorted(comm_result, key=lambda x: datetime.strptime(x['Date'], '%I:%M %p'), reverse=True)

    final_result = result + sorted_comm_result

    return{'result':final_result}

def final_uploadcomm():
    table = get_table('Comments')

    parentID = str(uuid.uuid4())
    global commentId
    comment = request.form.get('comment')
    today = datetime.now(ZoneInfo('America/New_York')).strftime("%I:%M %p")

    upload = {'ParentID': parentID, 'CommentID': commentId, 'Text': comment, 'Date': today, 'Username': session['username']}

    table.put_item(Item=upload)

    return {'result':'OK'}



#**************************************************************** Final Project End ********************************************************************************************






def auto_login():
    cookie = request.cookies.get('remember')
    if cookie is None:
        return False

    table = get_table('Remember')
    result = table.get_item(Key={'key':cookie})
    if 'Item' not in result:
        return False

    remember = result['Item']
    email = remember['email']

    table = get_table('Users')
    result = table.get_item(Key={'email':email})
    user = result['Item']

    session['email'] = user['email']
    session['username'] = user['username']
    return True


def get_remember_key(email):
    table = get_table('Remember')
    key = str(uuid.uuid4()) + str(uuid.uuid4())
    item = {'key':key, 'email':email}
    table.put_item(Item=item)
    return key

def liststudents():
    table = get_table('Students')
    result = []
    for item in table.scan()['Items']:
        s = {'StudentID':item['StudentID'], 'FirstName':item['FirstName'], 'LastName':item['LastName']}
        result.append(s)

    return{'result':result}

def listfiles():
    bucket = get_public_bucket()
    items = []
    for item in bucket.objects.all():
        items.append(item.key)
    return {'url':STORAGE_URL, 'items':items}

def uploadfile():
    bucket = get_public_bucket()
    file = request.files["file"]
    filename = file.filename

    # Note: You can get other form elements like this: x = request.form.get('x')

    ct = 'image/jpeg'
    if filename.endswith('.png'):
        ct = 'image/png'

    bucket.upload_fileobj(file, filename, ExtraArgs={'ContentType': ct})
    return {'results':'OK'}

#**************************************************************** Project 4 **********************************************************************************
def p4_get_table(name):
    dbclient = boto3.resource(service_name='dynamodb',
                        region_name='us-east-1',
                        aws_access_key_id=AWSKEY,
                        aws_secret_access_key=AWSSECRET
                        )

    table = dbclient.Table(name)
    return table

def p4_listuploads():
    table = p4_get_table('Uploads')
    result = []
    for item in table.scan()['Items']:
        s = {'ImageID':item['ImageID'], 'Caption':item['Caption'], 'FileName':item['FileName']}
        result.append(s)

    return{'result':result}

def p4_get_public_bucket():
    s3client = boto3.resource(service_name='s3',
                          region_name='us-east-1',
                          aws_access_key_id=AWSKEY,
                          aws_secret_access_key=AWSSECRET
                          )
    bucket = s3client.Bucket(PUBLIC_BUCKET)
    return bucket

def p4_uploadfile():
    # p4_listuploads() # list all uploads

    bucket = p4_get_public_bucket() # get bucket of images
    table = p4_get_table('Uploads') # get table of uploads (image id and caption)

    caption = request.form.get('caption') # retrieve caption input from user
    file = request.files["file"]
    filename = file.filename # retrieve image input from user

    # assign a unique id to the image
    ct =  str(uuid.uuid4()) + '/jpeg'
    if filename.endswith('.png'):
        ct = str(uuid.uuid4()) + '/png'

    upload = {'ImageID': ct, 'Caption': caption, 'FileName': filename} # put image id and caption into an object

    bucket.upload_fileobj(file, filename, ExtraArgs={'ContentType': ct}) # upload image file to s3 bucket
    table.put_item(Item=upload)                                                 # upload image id and caption to dynamo db table

    p4_listuploads() # list updated uploads
    return {'results':'OK'}


#**************************************************************** Project 4 End ******************************************************************************

#**************************************************************** Project 5 Start ****************************************************************************
def p5_listblogs():
    table = get_table('Blogs')
    result = []
    for item in table.scan()['Items']:
        s = {'BlogID':item['BlogID'], 'Title':item['Title'], 'Text':item['Text'], 'Date':item['Date']}
        result.append(s)

    sorted_result = sorted(result, key=lambda x: datetime.strptime(x['Date'], '%Y-%m-%d %H:%M:%S'), reverse=True)

    return{'result':sorted_result}

def p5_uploadblog():
    table = p4_get_table('Blogs')

    blogID = str(uuid.uuid4())
    title = request.form.get('title')
    text = request.form.get('text')
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    upload = {'BlogID': blogID, 'Title': title, 'Text': text, 'Date': today}

    table.put_item(Item=upload)

    p5_listblogs()
    return {'results':'OK'}

def p5_deleteblog():
    table = p4_get_table('Blogs')

    blog_id = request.form.get('blog_id')

    table.delete_item(Key={'BlogID': blog_id})

    p5_listblogs()
    return {'results':'OK'}
#**************************************************************** Project 5 End ******************************************************************************

def home():
    return 'Welcome home!'

def about():
    return 'Python is a program language.'

def add():
    a = request.args.get('a')
    b = request.args.get('b')
    result = int(a) + int(b)

    return str(result) # need to return a string or dictionary
    #https://jr09427n.pythonanywhere.com/add?a=5&b=5

def schedule(search):
    f = open('/home/jr09427n/data/courses.json')
    courses = json.load(f)
    f.close()

    search = search.lower()
    result_list = []
    for course in courses:
        if search in course['number'].lower() or search in course['name'].lower():
            result_list.append(course)

    return {'result':result_list}
    #https://jr09427n.pythonanywhere.com/schedule/internet

def apartment():
    f = open('/home/jr09427n/data/apartments.json')
    apartments = json.load(f)
    f.close()

    search = request.args.get('search', '').lower()
    room = request.args.get('rooms', '').lower()
    sort = request.args.get('sort', '').lower()

    def filter_by_room(apartment, room_filter):
        if room_filter == 'any':
            return True
        elif room_filter == 'one':
            return apartment['bedrooms'] >= 1
        elif room_filter == 'two':
            return apartment['bedrooms'] >= 2
        else:
            return True


    def sort_results(apartments, sort_option):
        if sort_option == 'asc':
            return sorted(apartments, key=lambda x: x["monthly_rent"])
        elif sort_option == 'desc':
            return sorted(apartments, key=lambda x: x["monthly_rent"], reverse=True)
        else:
            return apartments

    result_list = []
    for apartment in apartments:
        title_match = search in apartment['title'].lower()
        description_match = search in apartment['description'].lower()
        room_match = filter_by_room(apartment, room)

        if (title_match or description_match) and room_match:
            result_list.append(apartment)

    sorted_result = sort_results(result_list, sort)
    return {'result': sorted_result}

def check_login():
    # return None

    return {'name':'Sebastien'}

def account():
    user = check_login()
    if user is None:
        return redirect('/')
    else:
        return 'Hello ' + user['name']

def find_course(number):
    number = number.lower()
    f = open('/home/jr09427n/data/courses.json')
    courses = json.load(f)
    f.close()

    for course in courses:
        if course['number'].lower() == number:
            return course

    return {}









