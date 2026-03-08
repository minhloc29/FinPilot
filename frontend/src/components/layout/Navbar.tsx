import { Bot, User, LogOut } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

export function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="flex items-center justify-between border-b border-border bg-card px-8 py-3">
      <div className="flex items-center gap-2">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
          <Bot className="h-4 w-4" />
        </div>
        <Link to="/" className="text-lg font-bold text-foreground">
          AlphaLens
        </Link>
      </div>

      <div className="hidden md:flex items-center gap-8">
        <a href="#" className="text-sm font-medium text-foreground hover:text-primary transition-colors">Home</a>
        <a href="#" className="text-sm font-medium text-muted-foreground hover:text-primary transition-colors">Portfolio</a>
        <a href="#" className="text-sm font-medium text-muted-foreground hover:text-primary transition-colors">Markets</a>
        <a href="#" className="text-sm font-medium text-muted-foreground hover:text-primary transition-colors">Research</a>
      </div>

      {user ? (
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline" className="rounded-full gap-2">
              <User className="h-4 w-4" />
              {user.username}
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" className="w-56">
            <DropdownMenuLabel>
              <div className="flex flex-col space-y-1">
                <p className="text-sm font-medium">{user.full_name || user.username}</p>
                <p className="text-xs text-muted-foreground">{user.email}</p>
              </div>
            </DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem asChild>
              <Link to={"/profile"}>Hồ sơ</Link>
            </DropdownMenuItem>
            <DropdownMenuItem>Cài đặt</DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem onClick={handleLogout} className="text-red-600">
              <LogOut className="h-4 w-4 mr-2" />
              Đăng xuất
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      ) : (
        <Link to="/login">
          <Button className="rounded-full gap-2 bg-primary text-primary-foreground hover:bg-primary/90">
            <User className="h-4 w-4" />
            Đăng nhập
          </Button>
        </Link>
      )}
    </nav>
  );
}
