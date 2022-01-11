
--station_cfg.ssid="Xiaomi_1B3E"
--station_cfg.pwd="51272162zjx"
Temp_Humi_Pin = 5                  --测温引脚号
station_wifi={}
station_wifi.ssid="Xiaomi_1B3E"   --wifi用户名
station_wifi.pwd="51272162zjx"    --wifi密码
mqtt_name = '00101'                --该发布者的连接名
mqtt_pub_interview = 4000          --发布信息的间隔时间（ms）
mqtt_pub_name = "temp_moist"       --mqtt发布的内容标题头

mqtt_waiting_port = 5000           --等待mqtt服务器寻找的端口，自动寻址
mqtt_ip = "0.0.0.0"                --mqtt服务器地址
mqtt_port = 1883                   --mqtt服务器端口号
mqtt_waiting_data = "findingmqtt"  --mqtt服务器发的连接请求信息



timer_wifi_wait = tmr.create()     --守护wifi连接状态
timer_mqttfinding_wait = tmr.create() --守护mqtt服务器连接

timer_wifi = tmr.create()          --连接wifi计时器
timer_publish = tmr.create()       --发布消息计时器

start_connect_wifi = 0             --是否正在连接wifi的标志
time_sec = 0                       --记录wifi连接时间

mqtt_server = 0                    --mqtt服务器状态，0表示尚未连接mqtt服务器
mqtt_connect = 0                   --mqtt是否正在等待连接
mqtt_connect_sec = 0               --当前mqtt等待连接的时间

--连接WiFi

function timer_wifi_wait_fun()
    if wifi.sta.getip() == nil then
        if start_connect_wifi == 0 then
            mqtt_connect = 0
            start_connect_wifi = 1
            print("start connect wifi")
            --连接wifi
            wifi.setmode(wifi.STATION)
            wifi.sta.config(station_wifi)
            wifi.sta.connect()
            timer_wifi:alarm(1000, tmr.ALARM_AUTO, Connectwifi)
        end
    end
end


function Connectwifi()
    if wifi.sta.getip() == nil then
        print("Connecting WiFi ... "..tostring(time_sec).."s")
        time_sec = time_sec+1
    else
        time_sec = 0
        timer_wifi:stop()
        start_connect_wifi = 0
        print("Connnect WiFi success")
        print("host ip: "..wifi.sta.getip())
        --star_mqtt()                --启动mqtt连接
    end
end


function finding_mqtt_server()
    if mqtt_server == 0 then
        if mqtt_connect == 0 then
            if wifi.sta.getip() ~= nil then
                mqtt_connect = 1
                print("waiting for mqtt server")
                --如果此时断网
                udpSocket = net.createUDPSocket()
                udpSocket:listen(mqtt_waiting_port)
                udpSocket:on("receive", function(s, data, port, ip)
                    if data == mqtt_waiting_data then
                        mqtt_ip = ip
                        print("mqtt service ip :"..ip)
                        udpSocket:close()
                        print("connect mqtt service")
                        start_mqtt()
                        mqtt_server = 1
                        mqtt_connect = 0
                        mqtt_connect_sec = 0
                    end
                end)
            end
        end
    end
end

function start_mqtt()
    --启动mqtt连接
    m = mqtt.Client(mqtt_name,120)
    m:connect(mqtt_ip,mqtt_port,0,function(client)
        print("mqtt connect successfully")
        --定时发布温湿度数据
        end,
        function(client,reason)
            print("mqtt connect fail:"..reason)
            mqtt_server = 0
            mqtt_connect = 0
        end
    )
    m:on("offline",function(client)
        print("mqtt server offline, please waiting")
        mqtt_server = 0
        mqtt_connect = 0
    end)
end

function mqttpublish()
    if mqtt_server == 1 then
        status,temp,humi,temp_dec,humi_dec = dht.read11(Temp_Humi_Pin)
        if temp == -999 then
            print("dht equipment not found")
        else
            print("temp:"..temp,"humi:"..humi)
            data = {}
            data.name = mqtt_name
            data.temp = temp
            data.humi = humi
            ok, json = pcall(sjson.encode, {params=data})
            m:publish(mqtt_pub_name,json,0,0,function(client)
                    --print("publish successful")
            end)
        end
    end
end

timer_publish:alarm(mqtt_pub_interview,tmr.ALARM_AUTO,mqttpublish)
timer_wifi_wait:alarm(2000, tmr.ALARM_AUTO, timer_wifi_wait_fun)
timer_mqttfinding_wait:alarm(5000, tmr.ALARM_AUTO, finding_mqtt_server)
