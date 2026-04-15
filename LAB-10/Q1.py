import numpy as np
import matplotlib.pyplot as plt
import csv
import os

# resolve path relative to this script, not the CWD
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Load cities data
data = []
with open(os.path.join(SCRIPT_DIR, "cities - cities.csv"), "r") as f:
    reader = csv.reader(f)
    for row in reader:
        data.append([float(row[0]), float(row[1])])

cities = np.array(data)
K = 3  # number of airports

# ============================================================
# Assign each city to nearest centroid, return cluster labels
# ============================================================
def assign_clusters(cities, centroids):
    labels = []
    for pt in cities:
        dists = [np.sum((pt - c)**2) for c in centroids]
        labels.append(np.argmin(dists))
    return np.array(labels)

def calc_sse(cities, centroids, labels):
    total = 0
    for i, pt in enumerate(cities):
        total += np.sum((pt - centroids[labels[i]])**2)
    return total

# ============================================================
# METHOD A: Gradient Descent (K-Means style via gradient update)
# For each centroid k:
#   gradient = -2 * sum_i_in_cluster_k (x_i - c_k)
# Update: c_k = c_k - lr * gradient
# This is mathematically equivalent to the mean update in K-Means
# but uses explicit gradient steps.
# ============================================================
def gradient_descent_kmeans(cities, K=3, lr=0.1, max_iter=200, tol=1e-6):
    np.random.seed(100)
    idx = np.random.choice(len(cities), K, replace=False)
    centroids = cities[idx].copy().astype(float)
    
    sse_history = []
    
    for iteration in range(max_iter):
        labels = assign_clusters(cities, centroids)
        sse = calc_sse(cities, centroids, labels)
        sse_history.append(sse)
        
        new_centroids = centroids.copy()
        for k in range(K):
            cluster_pts = cities[labels == k]
            if len(cluster_pts) == 0:
                continue
            # gradient of SSE w.r.t centroid k
            # use mean (not sum) so step size doesn't blow up with large clusters
            grad = -2 * np.mean(cluster_pts - centroids[k], axis=0)
            new_centroids[k] = centroids[k] - lr * grad
        
        diff = np.max(np.linalg.norm(new_centroids - centroids, axis=1))
        centroids = new_centroids
        
        if diff < tol:
            print(f"[GD] Converged at iteration {iteration+1}")
            break

    labels = assign_clusters(cities, centroids)
    sse = calc_sse(cities, centroids, labels)
    return centroids, labels, sse, sse_history


# ============================================================
# METHOD B: Newton-Raphson Method
# For each centroid k:
#   f(c_k)  = -2 * sum_i_in_cluster_k (x_i - c_k)    [gradient / first deriv]
#   f'(c_k) = 2 * n_k   (second deriv - Hessian diagonal)
# Update: c_k = c_k - f / f'
# Analytically this gives c_k = mean of cluster points
# We apply it iteratively with re-assignment steps.
# ============================================================
def newton_raphson_kmeans(cities, K=3, max_iter=200, tol=1e-6):
    np.random.seed(42)
    idx = np.random.choice(len(cities), K, replace=False)
    centroids = cities[idx].copy().astype(float)
    
    sse_history = []
    
    for iteration in range(max_iter):
        labels = assign_clusters(cities, centroids)
        sse = calc_sse(cities, centroids, labels)
        sse_history.append(sse)
        
        new_centroids = centroids.copy()
        for k in range(K):
            cluster_pts = cities[labels == k]
            if len(cluster_pts) == 0:
                continue
            n_k = len(cluster_pts)
            # first derivative (gradient)
            grad = -2 * np.sum(cluster_pts - centroids[k], axis=0)
            # second derivative (Hessian diagonal element) = 2 * n_k
            hess = 2 * n_k
            # Newton-Raphson step
            new_centroids[k] = centroids[k] - grad / hess
        
        diff = np.max(np.linalg.norm(new_centroids - centroids, axis=1))
        centroids = new_centroids
        
        if diff < tol:
            print(f"[NR] Converged at iteration {iteration+1}")
            break
    
    labels = assign_clusters(cities, centroids)
    sse = calc_sse(cities, centroids, labels)
    return centroids, labels, sse, sse_history


# ============================================================
# Run both methods
# ============================================================
print("=" * 55)
print("   AIRPORT LOCATION OPTIMIZATION - SURAT DISTRICT")
print("=" * 55)

print("\n--- Method A: Gradient Descent ---")
gd_centroids, gd_labels, gd_sse, gd_history = gradient_descent_kmeans(cities, K=3)

print("\nOptimal Airport Locations (GD):")
for i, c in enumerate(gd_centroids):
    pts_in = np.sum(gd_labels == i)
    print(f"  Airport {i+1}: ({c[0]:.4f}, {c[1]:.4f})  |  Cities served: {pts_in}")

print(f"\nTotal SSE (GD): {gd_sse:.4f}")

print("\n--- Method B: Newton-Raphson ---")
nr_centroids, nr_labels, nr_sse, nr_history = newton_raphson_kmeans(cities, K=3)

print("\nOptimal Airport Locations (NR):")
for i, c in enumerate(nr_centroids):
    pts_in = np.sum(nr_labels == i)
    print(f"  Airport {i+1}: ({c[0]:.4f}, {c[1]:.4f})  |  Cities served: {pts_in}")

print(f"\nTotal SSE (NR): {nr_sse:.4f}")

print("\n--- Comparison ---")
print(f"{'Method':<25} {'SSE':>12} {'Iterations to converge':>24}")
print("-" * 63)
print(f"{'Gradient Descent':<25} {gd_sse:>12.4f} {len(gd_history):>24}")
print(f"{'Newton-Raphson':<25} {nr_sse:>12.4f} {len(nr_history):>24}")


# ============================================================
# Plot 1: Cluster visualization for both methods
# ============================================================
colors = ['red', 'blue', 'green']
markers = ['o', 's', '^']

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("Airport Location Optimization - Surat District", fontsize=14, fontweight='bold')

for ax, centroids, labels, title in [
    (axes[0], gd_centroids, gd_labels, "Method A: Gradient Descent"),
    (axes[1], nr_centroids, nr_labels, "Method B: Newton-Raphson")
]:
    for k in range(K):
        pts = cities[labels == k]
        ax.scatter(pts[:, 0], pts[:, 1], c=colors[k], alpha=0.6, s=50, label=f"Cluster {k+1}")
        ax.scatter(centroids[k, 0], centroids[k, 1], c=colors[k], marker=markers[k],
                   s=250, edgecolors='black', linewidths=2, zorder=5)
    ax.set_title(title)
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")
    ax.legend()
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(SCRIPT_DIR, "airport_clusters.png"), dpi=150)
plt.show()


# ============================================================
# Plot 2: SSE convergence comparison
# ============================================================
plt.figure(figsize=(9, 5))
plt.plot(gd_history, label="Gradient Descent", color="blue", linewidth=2)
plt.plot(nr_history, label="Newton-Raphson", color="green", linewidth=2, linestyle="--")
plt.xlabel("Iteration")
plt.ylabel("SSE (Sum of Squared Distances)")
plt.title("Convergence Comparison: GD vs Newton-Raphson")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(SCRIPT_DIR, "convergence_comparison.png"), dpi=150)
plt.show()

print("\nPlots saved: airport_clusters.png, convergence_comparison.png")
