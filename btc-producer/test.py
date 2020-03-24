from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

rpc_user = 'foo'
rpc_password = 'qDDZdeQ5vw9XXFeVnXT4PZ--tGN2xNjjR4nrtyszZx0='
# rpc_user and rpc_password are set in the bitcoin.conf file
rpc_connection = AuthServiceProxy("http://%s:%s@bitcoin-node:8332"%(rpc_user, rpc_password))
best_block_hash = rpc_connection.getbestblockhash()
print(rpc_connection.getblock(best_block_hash))

# batch support : print timestamps of blocks 0 to 99 in 2 RPC round-trips:
commands = [ [ "getblockhash", height] for height in range(100) ]
block_hashes = rpc_connection.batch_(commands)
blocks = rpc_connection.batch_([ [ "getblock", h ] for h in block_hashes ])
block_times = [ block["time"] for block in blocks ]
print(block_times)