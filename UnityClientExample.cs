using System;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using UnityEngine;

public static class RemoteLogClient
{
    private static List<Log> queue = new List<Log>();

    static RemoteLogClient()
    {
        GetServerIP();
    }

    [Serializable]
    public class Log
    {
        public string message;
        public LogType type;
        public float timestamp;
    }

    public enum LogType
    {
        Debug = 0,
        Waring = 1,
        Error = 2,
    }
    private const int UDP_PORT_NUMBER = 39502;
    private static string broadcast_password = "remote-logger";
    private const int TCP_PORT_NUMBER = 30270;


    private static string serverIp;

    private static async Task GetServerIP()
    {
        UdpClient client = new UdpClient();
        IPEndPoint ip = new IPEndPoint(IPAddress.Any, UDP_PORT_NUMBER);
        client.Client.SetSocketOption(SocketOptionLevel.Socket, SocketOptionName.Broadcast, true);

        client.ExclusiveAddressUse = false;
        client.Client.Bind(ip);

        var result = await client.ReceiveAsync();


        string message = Encoding.UTF8.GetString(result.Buffer);

        if (message == broadcast_password)
        {
            serverIp = result.RemoteEndPoint.Address.ToString();
        }
        else
        {
            GetServerIP();
        }
    }


    public static async void SendMessageToServer(string message)
    {
        var log = new Log {message = message, type = LogType.Debug, timestamp = UnixTimeNow()};

        if (string.IsNullOrEmpty(serverIp))
        {
            queue.Add(log);
        }
        else
        {
            if (queue.Count > 0)
            {
                queue.ForEach(SendLog);
                queue.Clear();
            }

            SendLog(log);
        }
    }

    private static async void SendLog(Log log)
    {
        var json = JsonUtility.ToJson(log);
        byte[] bytes = Encoding.UTF8.GetBytes(json);


        var tcp = new TcpClient(serverIp, TCP_PORT_NUMBER);
        tcp.Client.Send(bytes);
    }

    private static long UnixTimeNow()
    {
        var timeSpan = (DateTime.UtcNow - new DateTime(1970, 1, 1, 0, 0, 0));

        return (long) timeSpan.TotalSeconds;
    }
}

