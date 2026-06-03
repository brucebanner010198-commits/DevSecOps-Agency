```markdown
# DevSecOps-Agency Development Patterns

> Auto-generated skill from repository analysis

## Overview

This skill documents the core development patterns and workflows used in the `DevSecOps-Agency` TypeScript codebase. It covers file organization, coding conventions, and structured research workflows for adding and finalizing research packs. The repository emphasizes organized research documentation, modular code, and clear contribution processes.

## Coding Conventions

- **File Naming:**  
  Use kebab-case for all file names.
  ```
  good-example: competitive-landscape.ts
  bad-example: CompetitiveLandscape.ts
  ```

- **Import Style:**  
  Use relative imports.
  ```typescript
  import { analyzeMatrix } from './matrix-utils';
  ```

- **Export Style:**  
  Use named exports.
  ```typescript
  // matrix-utils.ts
  export function analyzeMatrix() { /* ... */ }
  ```

- **Markdown Research Packs:**  
  Research content is organized under `research/` in subfolders, each representing a research pack. Files are sequentially numbered for order and clarity.
  ```
  research/competitive-landscape/00-README.md
  research/competitive-landscape/01-overview-and-matrix.md
  research/competitive-landscape/02-executive-summary.md
  research/competitive-landscape/DELIVERY-NOTES.md
  research/competitive-landscape/_TEMPLATE.md
  ```

## Workflows

### Add Research Pack
**Trigger:** When introducing a comprehensive research analysis or landscape review.  
**Command:** `/new-research-pack`

1. Create a new subfolder under `research/` (e.g., `research/competitive-landscape/`).
2. Add multiple structured markdown files, such as:
   - `00-README.md` (index/overview)
   - `01-overview-and-matrix.md` (detailed analysis)
   - Additional numbered files as needed
3. Include a `_TEMPLATE.md` for future contributors to follow.
4. Example structure:
   ```
   research/competitive-landscape/
     ├── 00-README.md
     ├── 01-overview-and-matrix.md
     ├── _TEMPLATE.md
   ```

### Update Research Pack with Summary and Notes
**Trigger:** When finalizing a research pack with an executive summary and delivery notes.  
**Command:** `/finalize-research-pack`

1. Add an executive summary markdown file (e.g., `02-executive-summary.md`) to the research pack folder.
2. Add `DELIVERY-NOTES.md` to capture delivery state and caveats.
3. Update the index file (`00-README.md`) to link to the new summary and notes.
4. Example update:
   ```
   research/competitive-landscape/
     ├── 00-README.md         # Updated with links to new files
     ├── 01-overview-and-matrix.md
     ├── 02-executive-summary.md
     ├── DELIVERY-NOTES.md
     ├── _TEMPLATE.md
   ```

## Testing Patterns

- **Test File Naming:**  
  Test files use the pattern `*.test.*` (e.g., `matrix-utils.test.ts`).
- **Framework:**  
  The testing framework is not explicitly detected; follow standard TypeScript testing practices.
- **Example Test File:**
  ```typescript
  // matrix-utils.test.ts
  import { analyzeMatrix } from './matrix-utils';

  describe('analyzeMatrix', () => {
    it('should analyze the matrix correctly', () => {
      // test implementation
    });
  });
  ```

## Commands

| Command                | Purpose                                                        |
|------------------------|----------------------------------------------------------------|
| /new-research-pack     | Scaffold a new research pack with structured markdown files    |
| /finalize-research-pack| Add executive summary, delivery notes, and update research pack|
```
