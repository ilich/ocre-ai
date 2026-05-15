import { useCallback, useEffect, useRef, useState } from "react";
import Box from "@mui/material/Box";
import CircularProgress from "@mui/material/CircularProgress";
import Divider from "@mui/material/Divider";
import IconButton from "@mui/material/IconButton";
import InputAdornment from "@mui/material/InputAdornment";
import Paper from "@mui/material/Paper";
import TextField from "@mui/material/TextField";
import Tooltip from "@mui/material/Tooltip";
import Typography from "@mui/material/Typography";
import AddCommentIcon from "@mui/icons-material/AddComment";
import CloseIcon from "@mui/icons-material/Close";
import SendIcon from "@mui/icons-material/Send";
import { useChatStore } from "~/store/chat";
import { useChat } from "../hooks/useChat";
import ChatMessage from "./ChatMessage";

const MIN_WIDTH = 280;
const MIN_HEIGHT = 300;
const DEFAULT_WIDTH = 380;
const DEFAULT_HEIGHT = 520;

export default function ChatPopup() {
  const { isOpen, history, clearHistory, close } = useChatStore();
  const { sendMessage, loading } = useChat();
  const [input, setInput] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);

  const [size, setSize] = useState({ width: DEFAULT_WIDTH, height: DEFAULT_HEIGHT });
  const dragStart = useRef<{ x: number; y: number; w: number; h: number } | null>(null);

  // Auto-scroll to latest message
  useEffect(() => {
    if (isOpen) {
      bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [history, isOpen]);

  const onResizeMouseDown = useCallback(
    (e: React.MouseEvent) => {
      e.preventDefault();
      dragStart.current = { x: e.clientX, y: e.clientY, w: size.width, h: size.height };

      function onMove(ev: MouseEvent) {
        if (!dragStart.current) return;
        // Popup anchored at bottom-right: dragging left/up grows the popup
        const dw = dragStart.current.x - ev.clientX;
        const dh = dragStart.current.y - ev.clientY;
        setSize({
          width: Math.max(MIN_WIDTH, dragStart.current.w + dw),
          height: Math.max(MIN_HEIGHT, dragStart.current.h + dh),
        });
      }

      function onUp() {
        dragStart.current = null;
        document.removeEventListener("mousemove", onMove);
        document.removeEventListener("mouseup", onUp);
      }

      document.addEventListener("mousemove", onMove);
      document.addEventListener("mouseup", onUp);
    },
    [size]
  );

  function handleSend() {
    const text = input.trim();
    if (!text || loading) return;
    setInput("");
    sendMessage(text);
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  if (!isOpen) return null;

  return (
    <Paper
      elevation={8}
      sx={{
        position: "fixed",
        bottom: 88,
        right: 24,
        width: size.width,
        height: size.height,
        zIndex: 1200,
        display: "flex",
        flexDirection: "column",
        borderRadius: 3,
        overflow: "hidden",
      }}
    >
      {/* Resize handle — top-left corner */}
      <Box
        onMouseDown={onResizeMouseDown}
        sx={{
          position: "absolute",
          top: 0,
          left: 0,
          width: 18,
          height: 18,
          cursor: "nw-resize",
          zIndex: 1,
          // Visual grip dots
          backgroundImage: `radial-gradient(circle, grey 1px, transparent 1px)`,
          backgroundSize: "5px 5px",
          backgroundPosition: "2px 2px",
          backgroundRepeat: "repeat",
          opacity: 0.35,
          "&:hover": { opacity: 0.7 },
          borderRadius: "12px 0 0 0",
        }}
      />

      {/* Header */}
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          px: 2,
          py: 1.5,
          bgcolor: "primary.main",
          color: "primary.contrastText",
          flexShrink: 0,
        }}
      >
        <Typography variant="subtitle1" sx={{ fontWeight: 600, flex: 1 }}>
          Chat
        </Typography>
        <Tooltip title="New chat">
          <IconButton size="small" color="inherit" onClick={clearHistory}>
            <AddCommentIcon fontSize="small" />
          </IconButton>
        </Tooltip>
        <Tooltip title="Close">
          <IconButton size="small" color="inherit" onClick={close} sx={{ ml: 0.5 }}>
            <CloseIcon fontSize="small" />
          </IconButton>
        </Tooltip>
      </Box>

      <Divider />

      {/* Messages */}
      <Box sx={{ flex: 1, overflowY: "auto", px: 2, py: 1.5 }}>
        {history.length === 0 && (
          <Typography variant="body2" color="text.secondary" sx={{ textAlign: "center", mt: 4 }}>
            Ask anything about the coins in context.
          </Typography>
        )}
        {history.map((msg, i) => (
          <ChatMessage key={i} message={msg} />
        ))}
        {loading && (
          <Box sx={{ display: "flex", justifyContent: "flex-start", mb: 1 }}>
            <CircularProgress size={20} />
          </Box>
        )}
        <div ref={bottomRef} />
      </Box>

      <Divider />

      {/* Input */}
      <Box sx={{ px: 2, py: 1.5, flexShrink: 0 }}>
        <TextField
          fullWidth
          size="small"
          multiline
          maxRows={3}
          placeholder="Ask a question…"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={loading}
          slotProps={{
            input: {
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton
                    size="small"
                    onClick={handleSend}
                    disabled={loading || !input.trim()}
                    color="primary"
                  >
                    <SendIcon fontSize="small" />
                  </IconButton>
                </InputAdornment>
              ),
            },
          }}
        />
      </Box>
    </Paper>
  );
}
