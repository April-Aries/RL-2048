import matplotlib.pyplot as plt
import re
from typing import List, Tuple, Dict

def parse_2048_training_data(data: str) -> Tuple[Dict[str, str], List[int], List[float], List[float]]:
    """
    Parse the 2048 RL training statistics data.
    
    Returns:
        metadata: Dictionary containing alpha, total, and seed
        episodes: List of episode numbers
        means: List of mean scores
    """
    lines = data.strip().split('\n')
    
    # Parse metadata
    metadata = {}
    episodes = [0]
    means = [0]
    prob2048 = [0.0]
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Parse metadata lines
        if line.startswith('alpha = '):
            metadata['alpha'] = line.split(' = ')[1]
        elif line.startswith('total = '):
            metadata['total'] = line.split(' = ')[1]
        elif line.startswith('seed = '):
            metadata['seed'] = line.split(' = ')[1]
        
        # Parse episode data lines (format: episode	mean = value	max = value)
        elif re.match(r'^\d+\s+mean\s*=\s*[\d.]+\s+max\s*=\s*[\d.]+', line):
            parts = re.split(r'\s+', line)

            prob2048.append(0.0)
            episode = int(parts[0])
            mean_match = re.search(r'mean\s*=\s*([\d.]+)', line)
            if mean_match:
                mean_score = float(mean_match.group(1))
                episodes.append(episode)
                means.append(mean_score)

        elif re.match(r'^\s*2048\s+[\d.]+%', line):
            prob_match = re.search(r'2048\s+([\d.]+)%', line)
            if prob_match:
                prob = float(prob_match.group(1))
                prob2048[-1] = prob
        
        i += 1
    
    return metadata, episodes, means, prob2048

def plot_2048_training_results(data: str, save_path: str = None):
    """
    Plot the 2048 RL training results.
    
    Args:
        data: Raw training statistics string
        save_path: Optional path to save the figure
    """
    metadata, episodes, means, prob2048 = parse_2048_training_data(data)
    
    # Create the plot
    plt.figure(figsize=(12, 8))
    
    # Plot the mean scores
    plt.plot(episodes, means, 'b-', linewidth=2, marker='o', markersize=4, alpha=0.8)
    
    # Set labels and title
    plt.xlabel('Episode', fontsize=14)
    plt.ylabel('Mean Score per Episode', fontsize=14)
    plt.title('TDL2048', fontsize=18, fontweight='bold')
    
    # Add grid
    plt.grid(True, alpha=0.3)
    
    # Set x-axis ticks with 10 steps
    if episodes:
        x_min = int( min(episodes) // 1000 ) * 1000
        x_max = int( max(episodes) // 1000 ) * 1000 + 1
        x_ticks = range( x_min, x_max, (x_max - x_min) // 10 )
        plt.xticks(x_ticks)
    
    # Add metadata information as text box
    info_text = []
    if 'alpha' in metadata:
        info_text.append(f"Alpha: {metadata['alpha']}")
    if 'total' in metadata:
        info_text.append(f"Total: {metadata['total']}")
    if 'seed' in metadata:
        info_text.append(f"Seed: {metadata['seed']}")
    
    if info_text:
        info_str = '\n'.join(info_text)
        plt.text(0.02, 0.98, info_str, transform=plt.gca().transAxes, 
                fontsize=12, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Adjust layout
    plt.tight_layout()
    
    # Save if path provided
    if save_path:
        plt.savefig(f'{save_path}-mean.png', dpi=300, bbox_inches='tight')

    # Create another plot
    plt.close()
    plt.figure(figsize=(12, 8))
    
    # Plot the mean scores
    plt.plot(episodes, prob2048, 'b-', linewidth=2, marker='o', markersize=4, alpha=0.8)
    
    # Set labels and title
    plt.xlabel('Episode', fontsize=14)
    plt.ylabel('Probability of 2048-tile (%)', fontsize=14)
    plt.title('TDL2048', fontsize=18, fontweight='bold')
    
    # Add grid
    plt.grid(True, alpha=0.3)
    
    # Set x-axis ticks with 10 steps
    if episodes:
        x_min = int( min(episodes) // 1000 ) * 1000
        x_max = int( max(episodes) // 1000 ) * 1000 + 1
        x_ticks = range( x_min, x_max, (x_max - x_min) // 10 )
        plt.xticks(x_ticks)
    
    # Add metadata information as text box
    info_text = []
    if 'alpha' in metadata:
        info_text.append(f"Alpha: {metadata['alpha']}")
    if 'total' in metadata:
        info_text.append(f"Total: {metadata['total']}")
    if 'seed' in metadata:
        info_text.append(f"Seed: {metadata['seed']}")
    
    if info_text:
        info_str = '\n'.join(info_text)
        plt.text(0.02, 0.98, info_str, transform=plt.gca().transAxes, 
                fontsize=12, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Adjust layout
    plt.tight_layout()
    
    # Save if path provided
    if save_path:
        plt.savefig(f'{save_path}-2048.png', dpi=300, bbox_inches='tight')

# Example usage
if __name__ == "__main__":
    # Read data from the uploaded file
    with open('statistics.txt', 'r') as f:
        data = f.read()
    
    # To save the plot, uncomment:
    plot_2048_training_results(data, save_path='result')
