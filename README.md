A simple Netwrok protocol designed to invoke specific actions in the server machine. Each message comprises a command indicating the intended action or containing binary data for execution.


message length + message

message length: 10 Bytes (unsigned integer, network byte order)

sequence diagram (created using plantuml.com):
