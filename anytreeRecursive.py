

import psycopg2
import sys, os

from anytree import Node, RenderTree, find_by_attr, findall_by_attr

os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

PGHOST="10.20.8.1"
PGDATABASE="AISI"
PGUSER="user"
PGPASSWORD="aisi"

# Set up a connection to the postgres server.
conn_string = "host="+ PGHOST +" port="+ "5432" +" dbname="+ PGDATABASE +" user=" + PGUSER \
+" password="+ PGPASSWORD
conn=psycopg2.connect(conn_string)



def recursive(ParentPartId,ParentNode,depth):
    sql = "SELECT \"ChildPartID\",\"ParentPartID\", \"Qty\" FROM public.\"tblPartBom\" WHERE \"ParentPartID\" Like " + "'" + ParentPartId +"'"
    #print(sql)
    cur=conn.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    for i in range(len(data)):
        print(data[i])

    if (len(data)!=0) and (depth<MaxDepth):
        for i in range(len(data)):
            if data[i][0]!= RootPartId:
                if data[i][0] not in NodeList:
                    CurrentParentNode=Node(data[i][0], parent= ParentNode,Qty= data[i][2])
                    NodeList.append(ParentPartId)
                    recursive(data[i][0],CurrentParentNode,depth+1)
                    NodeList.remove(ParentPartId)
                else:
                    print("Node ", data[i][0]," already an ancestor of ", ParentPartId, "Adding", data[i][0],"as a child to ",ParentPartId," will create a loop in tree")
                    input()
        


RootPartId=input('Root Part ID =')
MaxDepth=input('Max Depth (leave blank for full tree) =')
try:
    MaxDepth=int(MaxDepth)
except ValueError:
    MaxDepth=999
'''
if MaxDepth == "":
    MaxDepth = 9999
else:
    MaxDepth=int(MaxDepth)
'''
Root=Node(RootPartId)
NodeList =[]
recursive(RootPartId,Root,0)

#print(RenderTree(Root))

for pre, _, node in RenderTree(Root):
    print("%s%s" % (pre, node.name))

'''
from anytree.exporter import DotExporter
GraphOptions = ["splines=ortho", "node [shape=box]"]
DotExporter(Root,"digraph","tree",GraphOptions).to_dotfile("root1.dot")

from subprocess import check_call
cmd = ["dot", "root1.dot", "-T", "pdf", "-o", "root1.pdf"]
check_call(cmd)
'''
