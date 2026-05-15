import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeSanitize from "rehype-sanitize";
import Box from "@mui/material/Box";
import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import type { ChatHistoryItem } from "~/services/chat.service";

interface ChatMessageProps {
  message: ChatHistoryItem;
}

export default function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === "user";

  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: isUser ? "flex-end" : "flex-start",
        mb: 1,
      }}
    >
      <Paper
        elevation={0}
        sx={{
          px: 1.5,
          py: 1,
          maxWidth: "85%",
          bgcolor: isUser ? "primary.main" : "action.hover",
          color: isUser ? "primary.contrastText" : "text.primary",
          borderRadius: isUser ? "16px 16px 4px 16px" : "16px 16px 16px 4px",
          // Markdown element resets
          "& p": { m: 0, fontSize: "0.875rem", lineHeight: 1.5 },
          "& p + p": { mt: 0.75 },
          "& ul": { m: 0, pl: 2.5, fontSize: "0.875rem", listStyleType: "disc" },
          "& ol": { m: 0, pl: 2.5, fontSize: "0.875rem", listStyleType: "decimal" },
          "& li": { mb: 0.25 },
          "& code": {
            fontFamily: "monospace",
            fontSize: "0.8rem",
            bgcolor: isUser ? "rgba(0,0,0,0.15)" : "rgba(0,0,0,0.06)",
            px: 0.5,
            borderRadius: 0.5,
          },
          "& pre": {
            m: 0,
            mt: 0.5,
            p: 1,
            borderRadius: 1,
            bgcolor: isUser ? "rgba(0,0,0,0.2)" : "rgba(0,0,0,0.06)",
            overflow: "auto",
            fontSize: "0.8rem",
            fontFamily: "monospace",
          },
          "& pre code": { bgcolor: "transparent", p: 0 },
          "& strong": { fontWeight: 700 },
          "& em": { fontStyle: "italic" },
          "& a": { color: "inherit", textDecorationColor: "currentColor" },
          "& table": { borderCollapse: "collapse", width: "100%", fontSize: "0.8rem" },
          "& th, & td": { border: "1px solid", borderColor: "divider", px: 1, py: 0.5 },
          "& blockquote": {
            m: 0,
            pl: 1.5,
            borderLeft: "3px solid",
            borderColor: "divider",
            opacity: 0.8,
          },
          "& h1, & h2, & h3, & h4": {
            m: 0,
            mt: 0.5,
            mb: 0.25,
            fontSize: "0.9rem",
            fontWeight: 700,
          },
        }}
      >
        {isUser ? (
          <Typography variant="body2" sx={{ whiteSpace: "pre-wrap", wordBreak: "break-word" }}>
            {message.content}
          </Typography>
        ) : (
          <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeSanitize]}>
            {message.content}
          </ReactMarkdown>
        )}
      </Paper>
    </Box>
  );
}
