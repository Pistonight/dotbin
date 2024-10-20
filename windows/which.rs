use std::process::ExitCode;

use clap::Parser;

/// which [-a] COMMAND
#[derive(Debug, Clone, Parser)]
struct Cli {
    pub command: String,
    #[clap(short, long)]
    pub all: bool,
}

fn main() -> ExitCode {
    let cli = Cli::parse();
    if cli.all {
        let iter = match which::which_all_global(&cli.command) {
            Ok(x) => x,
            Err(e) => {
                let paths = std::env::var("PATH").unwrap_or_default();
                eprintln!("which: no {} in ({}): {:?}", cli.command, paths, e);
                return ExitCode::FAILURE;
            }
        };

        for path in iter {
            println!("{}", path.display())
        }
    } else {
        match which::which_global(&cli.command) {
            Ok(path) => println!("{}", path.display()),
            Err(e) => {
                let paths = std::env::var("PATH").unwrap_or_default();
                eprintln!("which: no {} in ({}): {:?}", cli.command, paths, e);
                return ExitCode::FAILURE;
            }
        }
    }

    ExitCode::SUCCESS
    
}