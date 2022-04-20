import aws_dynamodb as awsd

if(awsd.check_env()):
    client = awsd.Client()
    client.instantiate()
    #client.create_table("new_table");
    client.select_table("new_table")
    d = {'test4':"test5"}
    print(client.put_item("test3",d))
    a=client.get_item('test')
    print(a)

else:
    exit()