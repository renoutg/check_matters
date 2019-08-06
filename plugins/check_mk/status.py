# -*- coding: utf-8 -*-
import re, requests, json, six
from pytablewriter import MarkdownTableWriter
from mmpy_bot.bot import listen_to
from mmpy_bot.bot import respond_to

import cmk_settings

def pretty_headers(headers):
  for i in range(len(headers)):
    headers[i] = headers[i].capitalize().replace('_', ' ')
  return headers

def pretty_table_content(data):
  # find in which column the icons are
  index_to_remove = [ data[0].index(i) for i in data[0] if "icon" in i ]
  for row in data:
    row.pop(index_to_remove[0])
    for i in range(len(row)):
      #ensure cells are rendered properly
      if row[i] == "":
        row[i] = '&nbsp;'
      if row[i] == "CRIT":
        row[i] = ':fire: Critical'
      if row[i] == "WARN":
        row[i] = ':warning: Warning'
      if row[i] == "UNKN":
        row[i] = ':grey_question: Unknown'
  return data

def create_md_table(data, name):
    writer = MarkdownTableWriter()
    writer.table_name = name
    # use the headers provided by check mk as headers for our table
    writer.headers = pretty_headers(data.pop(0))
    writer.value_matrix = data
    # will normally print to stdout, catch in var
    writer.stream = six.StringIO()
    writer.write_table()
    return writer.stream.getvalue()
  

def cmk_services(message):
  #check for service problems
  svc_url = "{proto}{server}/{site}/check_mk/view.py?view_name={view}&is_service_acknowledged=0&output_format=JSON&_username={user}&_secret={password}".format(proto=cmk_settings.cmk_proto, server=cmk_settings.cmk_server, site=cmk_settings.cmk_site, view='svcproblems', user=cmk_settings.cmk_user, password=cmk_settings.cmk_pass)
  svc_request = requests.get(svc_url)
  svc_data = json.loads(svc_request.content)
  # if the list only contains 1 item, it's only the header
  if len(svc_data) == 1:
    message.send('# Service Problems \n:white_check_mark: No service problems')
  else:
    svc_data = pretty_table_content(svc_data)
    svc_md_table = create_md_table(svc_data, "Service problems")
    message.send(svc_md_table)

def cmk_hosts(message):
  # same for host problems
  host_url = "{proto}{server}/{site}/check_mk/view.py?view_name={view}&is_service_acknowledged=0&output_format=JSON&_username={user}&_secret={password}".format(proto=cmk_settings.cmk_proto, server=cmk_settings.cmk_server, site=cmk_settings.cmk_site, view='hostproblems', user=cmk_settings.cmk_user, password=cmk_settings.cmk_pass)
  host_request = requests.get(host_url)
  host_data = json.loads(host_request.content)
  if len(host_data) == 1:
    message.send('# Host Problems \n:white_check_mark: No hosts down')
  else:
    host_data = pretty_table_content(host_data)
    host_md_table = create_md_table(host_data, "Host problems")
    message.send(host_md_table)


# listen for anything that ends with "status" in a channel and respond
@listen_to('status$', re.IGNORECASE)
def cmk_status(message):
  cmk_services(message)
  cmk_hosts(message)

# respond to mentions and direct messages
@respond_to('status$', re.IGNORECASE)
def cmk_status(message):
  cmk_services(message)
  cmk_hosts(message)
