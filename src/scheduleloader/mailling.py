import config
import os
import time
import traceback
import email
import getpass, poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from datetime import datetime
# import file

def guess_charset(msg):
   # get charset from message object.
   charset = msg.get_charset()
   # if can not get charset
   if charset is None:
      # get message header content-type value and retrieve the charset from the value.
      content_type = msg.get('Content-Type', '').lower()
      pos = content_type.find('charset=')
      if pos >= 0:
         charset = content_type[pos + 8:].strip()
   return charset

def decode_str(s):
   if s == None:
      return s
   value, charset = decode_header(s)[0]
   if charset:
      value = value.decode(charset)
   return value
# variable indent_number is used to decide number of indent of each level in the mail multiple bory part.
def print_info(msg, indent_number=0):
   if indent_number == 0:
      # loop to retrieve from, to, subject from email header.
      for header in ['From', 'To', 'Subject', 'X-Original-MAILFROM', 'X-Original-SENDERIP', \
         'X-Original-SENDERCOUNTRY', 'Date', 'Content-Type', 'Content-Transfer-Encoding', 'Content-Disposition', 'X-FORWARD-ROUTE']:
         print("header:", header)
         # get header value
         value = msg.get(header, '')
         print("----", value)
         # print(header, ":", value)
         if value:
            # for subject header.
            if header=='Subject':
               # decode the subject value
               value = decode_str(value)
            # for from and to header. 
               print("        value:", value)
            elif header=='From' or header=='To':
               # parse email address
               hdr, addr = parseaddr(value)
               # decode the name value.
               name = decode_str(hdr)
               value = u'%s <%s>' % (name, addr)
               # print(header,":", name, ":", value)
               print("        name:", name, ", value:", value)
            else:
               value = decode_str(value)
               print("        value:", value)

         # print('indent_number', indent_number)
         # print('%s%s: %s' % (' ' * indent_number, header, value))
   # if message has multiple part. 
   # print("msg.is_multipart():", msg.is_multipart())

   if (msg.is_multipart()):
      # get multiple parts from message body.
      parts = msg.get_payload()
      # print("parts:",parts)
      # loop for each part
      for n, part in enumerate(parts):
         # if n != 0:
         #    break
         print('%spart %s' % (' ' * indent_number, n))
         print('%s--------------------' % (' ' * indent_number))
         # print multiple part information by invoke print_info function recursively.
         print_info(part, indent_number + 1)
   # if not multiple part. 
   else:
      # get message content mime type
      content_type = msg.get_content_type() 
      # print("content_type", content_type)
      # if plain text or html content type.
      if content_type=='text/plain' or content_type=='text/html':
         # get email content
         content = msg.get_payload(decode=True)
         # get content string charset
         charset = guess_charset(msg)
         # decode the content with charset if provided.
         if charset:
            content = content.decode(charset)
         # if indent_number == 1:
         #    print('%sText: %s' % (' ' * indent_number, content + '...'))             
         # if indent_number == 2:
         #    print('%sText: %s' % (' ' * indent_number, content + '...')) 
         # print('-----------------------------------------------------');
         # print('%sText: %s' % (' ' * indent_number, content + '...'))
         # print('=====================================================');
      elif content_type=='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' \
         or content_type=='application/vnd.ms-excel':
         print('%sExcel Attachment: %s' % (' ' * indent_number, content_type))
      else:
         print('%sAttachment: %s' % (' ' * indent_number, content_type))




def work():

   while True:
      try:
         server = poplib.POP3(config._pop3_host,config._pop3_port)
         server.user(config._mail_user)
         server.pass_(config._mail_pass)

         print('mail listening')
         for i in range(0, len(server.list()[1])):
            print('***************************************************************************************')
            print('mail count:',i)
            resp, lines, octets = server.retr(i+1)
            msg_content = b'\r\n'.join(lines).decode('utf-8')
            msg = Parser().parsestr(msg_content)
            # print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            # print(msg)
            # print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            subject = msg.get('Subject', '')
            subject = decode_str(subject)
            mail_from = msg.get('X-Original-MAILFROM', '')
            mail_from = decode_str(mail_from)
            
            if "" == mail_from:
               mail_from = msg.get('From', '')
               mail_from = decode_str(mail_from)


            allowed_mimetypes = ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]
            
            for part in msg.walk():
               if part.get_content_type() in allowed_mimetypes:
                  file_name = part.get_filename()
                  file_name = decode_str(file_name)
                  print("file_name", file_name)
                  
                  subpath = datetime.today().strftime('%Y%m%d')

                  file_data = part.get_payload(decode=True)
                  file_path = f"{config._path}{os.path.sep}{subpath}"

                  print("is:",os.path.isdir(file_path))
                  if not os.path.isdir(file_path):
                     os.mkdir(file_path)

                  full_path = f"{file_path}{os.path.sep}{mail_from}^{file_name}"
                  f = open(full_path,'wb')
                  f.write(file_data)
                  f.close()
         
            server.dele(i+1)
         server.quit()

      except Exception as identifier:
         print("mailling Exception:", identifier)
         traceback.print_exc()
         # pass

      time.sleep(10)






if __name__ == '__main__':
   # M = poplib.POP3_SSL('mail.klnet.co.kr',110)
   server = poplib.POP3('mail.klnet.co.kr',110)
   # server.set_debuglevel(1)
   # pop3_welcome = server.getwelcome().decode('utf-8')
   # print('welcome:',pop3_welcome)

   server.user("sked@klnet.co.kr")
   server.pass_("klnet2019!")
   # print('stat:',server.stat())

   # print(server.list())
   # print(server.list()[1])



# list() function return all email list
   # resp, mails, octets = server.list()
   # print(resp)
   # print(mails)
   # print(octets)
   # print('-------------------------------')
   # index = len(mails)
   # resp, lines, octets = server.retr(index)
   # msg_content = b'\r\n'.join(lines).decode('utf-8')
   # msg = Parser().parsestr(msg_content)
   # print(msg.get('From'))
   # print(resp)
   # print(lines)
   # print(octets)
   # print('-------------------------------')

   # for j in lines[:50]:
   #    print(j)

   # mails = len(server.list()[1])
   # print(range(mails))
   # print_info(mails)

   # print('가나다라마')
   # for i in range(3, 4):
   for i in range(0, len(server.list()[1])):
      print('***************************************************************************************')
      print('mail count:',i)
      # print(server.retr(i+1)[1])
      # msg = server.retr(i+1)[1]
      resp, lines, octets = server.retr(i+1)
      msg_content = b'\r\n'.join(lines).decode('utf-8')
      msg = Parser().parsestr(msg_content)
      # print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
      # print(msg)
      # print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
      subject = msg.get('Subject', '')
      subject = decode_str(subject)
      mail_from = msg.get('X-Original-MAILFROM', '')
      mail_from = decode_str(mail_from)
      
      if "" == mail_from:
         mail_from = msg.get('From', '')
         mail_from = decode_str(mail_from)

      print("================>",subject)
      print("================>",mail_from)
      # print("================>",mail_from2)
      # print('From:', msg.get('From'))
      
      # print_info(msg, )

      allowed_mimetypes = ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]
      
      for part in msg.walk():
         if part.get_content_type() in allowed_mimetypes:
            file_name = part.get_filename()
            file_name = decode_str(file_name)
            print("file_name", file_name)
            
            subpath = datetime.today().strftime('%Y%m%d')

            file_data = part.get_payload(decode=True)
            file_path = f"{config._path}{os.path.sep}{subpath}"

            print("is:",os.path.isdir(file_path))
            if not os.path.isdir(file_path):
               os.mkdir(file_path)

            full_path = f"{file_path}{os.path.sep}{mail_from}^{file_name}"
            f = open(full_path,'wb')
            f.write(file_data)
            f.close()
            # attachments.append(name)

            # print(name)
      #    if part.get_content_type():
      #       # body = part.get_payload(decode=True)
      #       print_info(msg, len(msg))

      # for j in range(0, len(server.retr(i+1)[1])):
      #    msg = server.retr(i+1)[1][j]

      #    print_info(server.retr(i+1)[1][j], j)
         # print(j)
         # print(server.retr(i+1)[1][j])

         # msg = server.retr(i+1)[1][j]
         # value = msg.get('Subject', '')
         # print(value)

         # msg = email.message_from_string((server.retr(i+1)[1][j]).decode("utf-8"))
         # strtext=msg.get_payload()
         # print (strtext)
            
         # if j > 10:
         #    break

   # for mail in server.list()[1]:
      # print(mail)


   # msg_content = b'\r\n'.join(lines).decode('utf-8')
   # msg_content = b'\r\n'.join(lines).decode('euc-kr')
   # msg_content = b'\r\n'.join(lines).decode('UTF-8')
   # msg = Parser().parsestr(msg_content)
   # email_from = msg.get('From')
   # email_to = msg.get('To')
   # email_subject = msg.get('Subject')
   # print('From ' + email_from)
   # print('To ' + email_to)
   # print('Subject ' + email_subject)
   server.quit()

    # numMessages = len(server.list()[1])
    # for i in range(numMessages):
    #     for j in server.retr(i+1)[1]:
    #         print(j)


