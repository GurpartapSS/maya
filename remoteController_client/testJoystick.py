import testclient as tc

cc =tc.remoteclient()
cc.connection()
cc.disconnect()

del cc

cc =tc.remoteclient()
cc.connection()
cc.disconnect()

del cc

# import botClient

# botClient.connection()
# botClient.disconnect()


# botClient.connection()
# botClient.disconnect()