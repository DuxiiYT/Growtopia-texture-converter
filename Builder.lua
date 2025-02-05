local Blocks_data = {}
local Blocks_needed = {}
local Delay = 0
local file1 = io.open("YOUR-PATH-HERE", "r") -- An example of your path could be C:\\Users\\Admin\\Desktop\\test\\output\\blocks_needed.txt
local file2 = io.open("YOUR-PATH-HERE", "r") -- An example of your path could be C:\\Users\\Admin\\Desktop\\test\\output\\blocks_needed.txt

local function CreateDialog(text)
    local textPacket = {
        [0] = "OnDialogRequest",
        [1] = text,
        netid = -1
    }
    SendVarlist(textPacket)
end

local function Place(x, y, id)
    local player = GetLocal()
    local punchPacket = {
      type = 3,
      int_data = id,
      pos_x = player.pos_x,
      pos_y = player.pos_y,
      int_x = x,
      int_y = y,
    }
    SendPacketRaw(punchPacket)
end

local function Menu()
    local dialog = [[
add_label_with_icon|big|`bMain Menu|left|11550|
add_spacer|small|
add_smalltext|`9Blocks Required:|
]]

    for name, amount in pairs(Blocks_needed) do
        dialog = dialog .. string.format("add_smalltext|%s: %d|\n", name, amount)
    end

    dialog = dialog .. [[
add_spacer|small|
add_url_button||`1Discord Community|noflags|https://discord.gg/jXbfXYVhAm|Join The Discord!|0|0|
add_spacer|small|
add_smalltext|Delay between placing blocks (Set at 100 by Default|
add_text_input|delay||100|4|
add_spacer|small|
add_button|start|`1Start|NOFLAGS|0|
add_quick_exit||
]]

    CreateDialog(dialog)
end

local function Start()
    RunThread(function()
        for _, block in ipairs(Blocks_data) do
            Place(block.x_tile, block.y_tile, block.itemid)
            Sleep(Delay)
        end
    end)
end

if file1 then
    for line in file1:lines() do
        local x, y, id = line:match("(%d+),%s*(%d+),%s*(%d+)")
        if id and x and y then
            table.insert(Blocks_data, {x_tile = tonumber(x), y_tile = tonumber(y), itemid = tonumber(id)})
        end
    end
    file1:close()
else
    print("Error: Could not open blocks_data.txt")
end

if file2 then
    for line in file2:lines() do
        local name, amount = line:match("(.+):%s*(%d+)")
        if name and amount then
            Blocks_needed[name] = tonumber(amount)
        end
    end
    file2:close()
else
    print("Error: Could not open blocks_needed.txt")
end

function CommandHandler(type, packet)
	if packet:find("action|input\n|text|") then
        if packet:find("/menu") then
            Menu()
            return true
        end
    elseif packet:find("buttonClicked|start") then
        Delay = packet:match("delay|(%d+)")
        if Delay then
            Start()
        end
    end
end

AddCallback("Command Handler", "OnPacket", CommandHandler)
