import { Bot, User } from "lucide-react";
import { Button } from "@/components/ui/button";

export function Navbar() {
  return (
    <nav className="flex items-center justify-between border-b border-border bg-card px-8 py-3">
      <div className="flex items-center gap-2">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
          <Bot className="h-4 w-4" />
        </div>
        <span className="text-lg font-bold text-foreground">FinAssist</span>
      </div>

      <div className="hidden md:flex items-center gap-8">
        <a href="#" className="text-sm font-medium text-foreground hover:text-primary transition-colors">Home</a>
        <a href="#" className="text-sm font-medium text-muted-foreground hover:text-primary transition-colors">Portfolio</a>
        <a href="#" className="text-sm font-medium text-muted-foreground hover:text-primary transition-colors">Markets</a>
        <a href="#" className="text-sm font-medium text-muted-foreground hover:text-primary transition-colors">Research</a>
      </div>

      <Button className="rounded-full gap-2 bg-primary text-primary-foreground hover:bg-primary/90">
        <User className="h-4 w-4" />
        Login
      </Button>
    </nav>
  );
}
