local mp = require 'mp'
function m()
    local width = mp.get_property("width")
    local height = mp.get_property("height")
    print(width, height)
    mp.command("quit")
end
mp.register_event("file-loaded", m)