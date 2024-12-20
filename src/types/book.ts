export enum BookStatus {
  DRAFT = 'draft',
  GENERATING = 'generating',
  COMPLETED = 'completed',
  FAILED = 'failed'
}

export interface BookGenerationConfig {
  title: string;
  description: string;
  genre: string;
  target_audience: string;
  style: string;
  tone: string;
  length: string;
}

export interface Book {
  id: number;
  title: string;
  description: string;
  genre: string;
  target_audience: string;
  style: string;
  tone: string;
  length: string;
  status: BookStatus;
  content?: {
    structure: string;
    content: string;
  };
}

export interface GenerationProgress {
  stage: 'planning' | 'writing' | 'dialogue' | 'review';
  message: string;
}