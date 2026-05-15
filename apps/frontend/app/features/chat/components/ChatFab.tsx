import Fab from "@mui/material/Fab";
import Tooltip from "@mui/material/Tooltip";
import ChatIcon from "@mui/icons-material/Chat";
import { useChatStore } from "~/store/chat";

export default function ChatFab() {
  const toggle = useChatStore((s) => s.toggle);

  return (
    <Tooltip title="Open chat" placement="left">
      <Fab
        color="primary"
        onClick={toggle}
        sx={{ position: "fixed", bottom: 24, right: 24, zIndex: 1200 }}
      >
        <ChatIcon />
      </Fab>
    </Tooltip>
  );
}
